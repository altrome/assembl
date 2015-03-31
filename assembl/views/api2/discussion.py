from functools import partial
import re
import base64
from os import urandom

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (HTTPOk, HTTPBadRequest, HTTPUnauthorized)
from pyramid_dogpile_cache import get_region
from pyramid.security import authenticated_userid

from assembl.auth import (
    P_READ, P_READ_PUBLIC_CIF, P_ADMIN_DISC, P_SYSADMIN, Everyone)
from assembl.auth.password import verify_data_token, data_token
from assembl.auth.util import get_permissions
from assembl.models import (Discussion, Permission)
from ..traversal import InstanceContext
from . import JSON_HEADER


@view_config(context=InstanceContext, request_method='GET',
             ctx_instance_class=Discussion, permission=P_READ,
             accept="application/json", name="settings",
             renderer='json')
def discussion_settings_get(request):
    return request.context._instance.settings_json


@view_config(context=InstanceContext, request_method='PUT',
             ctx_instance_class=Discussion, permission=P_ADMIN_DISC,
             header=JSON_HEADER, name="settings")
def discussion_settings_put(request):
    request.context._instance.settings_json = request.json_body
    return HTTPOk()


discussion_jsonld_cache = get_region('discussion_jsonld')
userprivate_jsonld_cache = get_region('userprivate_jsonld')

@discussion_jsonld_cache.cache_on_arguments()
def discussion_jsonld(discussion_id):
    from assembl.semantic.virtuoso_mapping import AssemblQuadStorageManager
    aqsm = AssemblQuadStorageManager()
    return aqsm.as_jsonld(discussion_id)


@userprivate_jsonld_cache.cache_on_arguments()
def userprivate_jsonld(discussion_id):
    from assembl.semantic.virtuoso_mapping import AssemblQuadStorageManager
    aqsm = AssemblQuadStorageManager()
    cg = aqsm.participants_private_as_graph(discussion_id)
    return aqsm.graph_as_jsonld(cg)



def read_user_token(request):
    salt = None
    user_id = authenticated_userid(request)
    discussion_id = request.context.get_discussion_id()
    permissions = get_permissions(user_id or Everyone, discussion_id)
    if P_READ in permissions:
        permissions.append(P_READ_PUBLIC_CIF)

    if 'token' in request.GET:
        token = request.GET['token'].encode('ascii')
        data = verify_data_token(token)
        if data is None:
            raise HTTPBadRequest("Invalid token")
        try:
            data, salt = data.split('.', 1)
            salt = base64.urlsafe_b64decode(salt)
            data = [int(i) for i in data.split(',')]
            t_user_id, t_discussion_id = data[:2]
            req_permissions = data[2:]
            if len(req_permissions):
                req_permissions = [x for (x,) in Permission.db.query(
                    Permission.name).filter(
                    Permission.id.in_(req_permissions)).all()]
        except (ValueError, IndexError):
            raise HTTPBadRequest("Invalid token")
        if discussion_id is not None and t_discussion_id != discussion_id:
            raise HTTPUnauthorized("Token for another discussion")
        if user_id is None:
            permissions = get_permissions(t_user_id, discussion_id)
        elif t_user_id != user_id:
            raise HTTPUnauthorized("Token for another user")
        user_id = t_user_id
        permissions = set(permissions).intersection(set(req_permissions))
    return user_id, permissions, salt


def handle_jsonp(callback_fn, json):
    if not re.match("^\w+$", callback_fn):
        raise HTTPBadRequest("invalid callback name")
    return "%s(%s);" % (callback_fn.encode('ascii'), json)


@view_config(context=InstanceContext, name="perm_token",
             ctx_instance_class=Discussion, request_method='GET',
             accept="application/ld+json")
def get_token(request):
    user_id = authenticated_userid(request)
    discussion_id = request.context.get_discussion_id()
    if not user_id:
        raise HTTPUnauthorized()
    req_permissions = request.GET.get('permission', ['read'])
    if isinstance(req_permissions, list):
        req_permissions = set(req_permissions)
    else:
        req_permissions = set((req_permissions,))
    permissions = set(get_permissions(user_id, discussion_id))
    if not req_permissions:
        req_permissions = permissions
    else:
        if P_READ in permissions:
            permissions.add(P_READ_PUBLIC_CIF)
        if P_SYSADMIN not in permissions:
            req_permissions = list(req_permissions.intersection(permissions))
    req_permissions = list(req_permissions)
    data = [str(user_id), str(discussion_id)]
    data.extend([str(x) for (x,) in Permission.db.query(Permission.id).filter(
        Permission.name.in_(req_permissions)).all()])
    data = ','.join(data) + '.' + base64.urlsafe_b64encode(urandom(8))
    return Response(body=data_token(data), content_type="text/text")


@view_config(context=InstanceContext, name="jsonld",
             ctx_instance_class=Discussion, request_method='GET',
             accept="application/ld+json")
@view_config(context=InstanceContext,
             ctx_instance_class=Discussion, request_method='GET',
             accept="application/ld+json")
def discussion_instance_view_jsonld(request):
    discussion = request.context._instance
    user_id, permissions, salt = read_user_token(request)
    if not (P_READ in permissions or P_READ_PUBLIC_CIF in permissions):
        raise HTTPUnauthorized()
    if not salt and P_ADMIN_DISC not in permissions:
        salt = base64.urlsafe_b64encode(urandom(6))

    jdata = discussion_jsonld(discussion.id)
    if salt:
        from assembl.semantic.virtuoso_mapping import (
            AssemblQuadStorageManager, hash_obfuscator)
        obfuscator = partial(hash_obfuscator, salt=salt)
        jdata = AssemblQuadStorageManager.obfuscate(jdata, obfuscator)
    # TODO: Add age
    if "callback" in request.GET:
        jdata = handle_jsonp(request.GET['callback'], jdata)
        content_type = "application/json-p"
    else:
        content_type = "application/ld+json"
    return Response(body=jdata, content_type=content_type)


@view_config(context=InstanceContext, name="private_jsonld",
             ctx_instance_class=Discussion, request_method='GET',
             accept="application/ld+json")
def user_private_view_jsonld(request):
    discussion_id = request.context.get_discussion_id()
    user_id, permissions, salt = read_user_token(request)
    if P_READ not in permissions:
        raise HTTPUnauthorized()
    if not salt and P_ADMIN_DISC not in permissions:
        salt = base64.urlsafe_b64encode(urandom(6))

    jdata = userprivate_jsonld(discussion_id)
    if salt:
        from assembl.semantic.virtuoso_mapping import (
            AssemblQuadStorageManager, hash_obfuscator)
        obfuscator = partial(hash_obfuscator, salt=salt)
        jdata = AssemblQuadStorageManager.obfuscate(jdata, obfuscator)
    if "callback" in request.GET:
        jdata = handle_jsonp(request.GET['callback'], jdata)
        content_type = "application/json-p"
    else:
        content_type = "application/ld+json"
    return Response(body=jdata, content_type=content_type)
