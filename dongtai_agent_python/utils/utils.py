import base64
import hashlib

from dongtai_agent_python.setting import const
from dongtai_agent_python.utils import scope


@scope.with_scope(scope.SCOPE_AGENT)
def normalize_response_header(status_line, headers):
    header_str = status_line + "\n" + json_to_str(headers)
    header_str = base64.b64encode(header_str.encode('utf-8'))
    header_str = bytes.decode(header_str, 'utf-8')
    return header_str


@scope.with_scope(scope.SCOPE_AGENT)
def json_to_base64(json_data):
    if json_data:
        json_data = json_to_str(json_data)
        json_data = base64.b64encode(json_data.encode('utf-8'))
        json_data = bytes.decode(json_data, 'utf-8')
    return json_data


@scope.with_scope(scope.SCOPE_AGENT)
def bytes_to_base64(data):
    b64_data = base64.b64encode(data)
    return bytes.decode(b64_data, 'utf-8')


@scope.with_scope(scope.SCOPE_AGENT)
def json_to_str(json_data):
    if json_data:
        new_list = []
        for item in json_data.keys():
            new_list.append(str(item) + "=" + str(json_data[item]))
        json_data = "\n".join(new_list)
    return json_data


def is_empty(value):
    if value is None:
        return True
    if isinstance(value, (tuple, list, dict, str, bytes, bytearray)):
        return not value
    return False


def is_not_allowed_type(value):
    return type(value) == int or type(value) == bool


def needs_propagation(context, node_type):
    if context is None or context.hook_exit or \
            (node_type != const.NODE_TYPE_SOURCE and not context.has_source):
        return False

    return True


@scope.with_scope(scope.SCOPE_AGENT)
def get_hash(item):
    try:
        h = hashlib.md5((str(type(item)) + ":" + str(id(item)) + ":" + str(item)).encode('utf-8')).hexdigest()
    except Exception:
        h = id(item)
    return h
