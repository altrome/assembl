from celery import Celery

from pyramid.path import DottedNameResolver

from . import init_task_config, config_celery_app

# broker specified
translation_celery_app = Celery('celery_tasks.translate')

resolver = DottedNameResolver(__package__)

_services = {}


def get_service_of_discussion(discussion):
    global _services
    service = discussion.preferences["translation_service"]
    if not service:
        return
    if service not in _services:
        cls = resolver.resolve(service)
        _services[service] = cls()
    return _services[service]


def translate_content(content, extra_languages=None):
    from ..models import Locale
    global services
    discussion = content.discussion
    service = get_service_of_discussion(discussion)
    if not service:
        return
    languages = discussion.discussion_locales
    languages.extend(extra_languages or ())
    languages = [Locale.get_or_create(locname) for locname in languages]
    base_languages = {loc: service.asKnownLocale(loc.locale) for loc in languages}
    undefined_id = Locale.UNDEFINED_LOCALEID
    changed = False
    previous_locale_id = None
    for prop in ("body", "subject"):
        ls = getattr(content, prop)
        if ls:
            entries = ls.entries_as_dict
            if undefined_id in entries:
                entry = entries[undefined_id]
                if entry.value and service.can_guess_locale(entry.value or ''):
                    service.confirm_locale(entry, languages)
                    # reload entries
                    ls.db.expire(ls, ("entries_as_dict",))
                    entries = ls.entries_as_dict
                elif entry.value and prop == 'subject':
                    # assume same locale as body's original
                    # (Usually only one of those...)
                    entry.locale_id = previous_locale_id
            known = {service.asKnownLocale(
                        Locale.extract_source_locale(
                            Locale.locale_collection_byid[loc_id]))
                     for loc_id in entries}
            originals = ls.non_mt_entries()
            # pick randomly. TODO: Recency order?
            original = next(iter(originals))
            for lang in languages:
                base = base_languages[lang]
                if base not in known:
                    service.translate_lse(original, lang)
                    changed = True
            ls.db.expire(ls, ["entries"])
            previous_locale_id = original.locale_id
    if changed:
        content.send_to_changes()
        ls.db.commit()


@translation_celery_app.task(ignore_result=True)
def translate_content_task(content_id, extra_languages=None):
    global services
    init_task_config(translation_celery_app)
    from ..models import Content
    content = Content.get(content_id)
    translate_content(content, extra_languages)


@translation_celery_app.task(ignore_result=True)
def translate_discussion(discussion_id, extra_languages=None):
    extra_languages = extra_languages or []
    from ..models import Discussion
    discussion = Discussion.get(discussion_id)
    service = get_service_of_discussion(discussion)
    if not service:
        return
    languages = discussion.discussion_locales
    languages.extend(extra_languages or ())
    languages = {service.asKnownLocale(loc) for loc in languages}
    for post in discussion.posts:
        missing = False
        for prop in ("body", "subject"):
            ls = getattr(post, prop)
            post_langs = {service.asKnownLocale(loc)
                          for loc in ls.entries_as_dict}
            if languages - post_langs:
                missing = True
                break
        if missing:
            translate_content(post, extra_languages)


def includeme(config):
    config_celery_app(translation_celery_app, config.registry.settings)