from abc import abstractmethod
import urllib2

import simplejson as json
from langdetect import detect_langs

from assembl.lib.abc import abstractclassmethod
from assembl.models import Locale, LangStringEntry


class TranslationService(object):

    @abstractclassmethod
    def canTranslate(cls, source, target):
        return False

    @classmethod
    def asKnownLocale(cls, locale_name):
        return locale_name

    def identify(self, text):
        language_data = detect_langs(text.value)
        return language_data[0].lang, {x.lang: x.prob for x in language_data}

    def confirm_locale(self, langstring_entry):
        lang, data = self.identify(langstring_entry)
        data["_service"] = self.__class__.__name__
        hypothesis = langstring_entry.locale
        if (hypothesis.sublocale_of(lang)
                or hypothesis.locale == Locale.UNDEFINED):
            if hypothesis.locale == Locale.UNDEFINED:
                langstring_entry.locale_name = lang
                langstring_entry.db.expire(langstring_entry, ["locale"])
            langstring_entry.locale_confirmed = True
            locale_identification_data = json.dumps(data)
        elif langstring_entry.locale_confirmed:
            # confirmed by a previous service with different result?
            # Todo: Compare thresholds of both services... if comparable.
            pass
        else:
            locale_identification_data = json.dumps(data)

    @abstractmethod
    def translate(self, text, target, source=None):
        if not source or source == Locale.UNDEFINED:
            lang, data = self.identify(text)
            source = Locale.get_or_create(source_name)
        return text

    def get_mt_name(cls, source_name, target_name):
        return "-".join((target_name, "x-mtfrom", source_name))

    def translate_lse(self, langstring_entry, target, retranslate=False):
        if langstring_entry.locale_name == Locale.UNDEFINED:
            self.confirm_locale(langstring_entry)
        source = langstring_entry.locale
        mt_target_name = self.get_mt_name(source.locale, target.locale)
        existing = langstring_entry.langstring.entries_as_dict.get(
            mt_target_name, None)
        if existing and not retranslate:
            return langstring_entry.langstring.entries_as_dict[mt_target_name]
        if not self.canTranslate(source, target):
            return existing
        trans = self.translate(langstring_entry.value, target, source)
        lse = LangStringEntry(
            value=trans,
            locale=Locale.get_or_create(mt_target_name),
            locale_identification_data=json.dumps(dict(
                translator=self.__class__.__name__)),
            langstring_id=langstring_entry.langstring_id)
        langstring_entry.db.add(lse)
        return lse


class DummyTranslationService(TranslationService):
    @classmethod
    def canTranslate(cls, source, target):
        return True

    def translate(self, text, target, source=None):
        return u"Pseudo-translation from %s to %s of: %s" % (
            source.locale, target.locale, text)


class DummyGoogleTranslationService(TranslationService):
    # Uses public Google API. For testing purposes. Do NOT use in production.
    known_locales = {
        "af", "sq", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca",
        "ceb", "ny", "zh-CN", "zh-TW", "hr", "cs", "da", "nl", "en", "eo",
        "et", "tl", "fi", "fr", "gl", "ka", "de", "el", "gu", "ht", "ha",
        "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw",
        "kn", "kk", "km", "ko", "lo", "la", "lv", "lt", "mk", "mg", "ms",
        "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "fa", "pl", "pt",
        "ma", "ro", "ru", "sr", "st", "si", "sk", "sl", "so", "es", "su",
        "sw", "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi",
        "cy", "yi", "yo", "zu"}
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}

    @classmethod
    def asKnownLocale(cls, locale_name):
        parts = locale_name.split("_")
        base = parts[0]
        if base in cls.known_locales:
            return base
        if base == "zh":
            p1 = parts[1]
            if p1 == "Hans":
                return "zh-CN"
            elif p1 == "Hant":
                return "zh-TW"
            elif p1 in ("CN", "TW"):
                return "_".join(parts[:1])

    def get_mt_name(cls, source_name, target_name):
        return super(DummyGoogleTranslationService, cls).get_mt_name(
            cls.asKnownLocale(source_name), cls.asKnownLocale(target_name))

    @classmethod
    def canTranslate(cls, source, target):
        return (cls.asKnownLocale(source.locale) and
                cls.asKnownLocale(target.locale))

    def translate(self, text, target, source=None):
        # Initial implementation from https://github.com/mouuff/Google-Translate-API
        link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (
            self.asKnownLocale(target.locale),
            self.asKnownLocale(source.locale) if source else "",
            text.replace(" ", "+"))
        request = urllib2.Request(link, headers=self.agents)
        page = urllib2.urlopen(request).read()
        before_trans = 'class="t0">'
        result = page[page.find(before_trans)+len(before_trans):]
        result = result.split("<")[0]
        return result


class GoogleTranslationService(DummyGoogleTranslationService):
    def __init__(self, apikey=None):
        # Look it up in config
        self.apikey = apikey

    def translate(self, text, target, source=None):
        # TODO
        pass
