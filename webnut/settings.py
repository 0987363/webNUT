import importlib
import os
from collections import namedtuple


NUTConfig = namedtuple(
    "NUTConfig",
    ["server", "port", "username", "password", "webnut_username", "webnut_password"],
)


def _load_file_config():
    try:
        return importlib.import_module(".config", __package__)
    except ModuleNotFoundError as error:
        if error.name == "%s.config" % __package__:
            return None
        raise


def _valid_string(name):
    value = os.environ.get(name)
    if value:
        return value
    return None


def _valid_port(name):
    value = os.environ.get(name)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def load_config():
    file_config = _load_file_config()

    server = getattr(file_config, "server", "127.0.0.1")
    port = getattr(file_config, "port", 3493)
    username = getattr(file_config, "username", None)
    password = getattr(file_config, "password", None)
    webnut_username = getattr(file_config, "webnut_username", None)
    webnut_password = getattr(file_config, "webnut_password", None)

    server = _valid_string("NUT_SERVER") or server
    port = _valid_port("NUT_PORT") or port
    username = _valid_string("NUT_USERNAME") or username
    password = _valid_string("NUT_PASSWORD") or password
    webnut_username = _valid_string("WEBNUT_USERNAME") or webnut_username
    webnut_password = _valid_string("WEBNUT_PASSWORD") or webnut_password

    return NUTConfig(server, port, username, password, webnut_username, webnut_password)
