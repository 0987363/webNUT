import base64
import sys
import types
import unittest
from unittest import mock


pyramid = types.ModuleType("pyramid")
pyramid_config = types.ModuleType("pyramid.config")
pyramid_httpexceptions = types.ModuleType("pyramid.httpexceptions")
pyramid_config.Configurator = object
pyramid_httpexceptions.HTTPNotFound = object
with mock.patch.dict(
    sys.modules,
    {
        "pyramid": pyramid,
        "pyramid.config": pyramid_config,
        "pyramid.httpexceptions": pyramid_httpexceptions,
    },
):
    from webnut.basic_auth import BasicAuthMiddleware


def ok_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"ok"]


class StartResponse(object):
    def __call__(self, status, headers):
        self.status = status
        self.headers = dict(headers)


class BasicAuthMiddlewareTests(unittest.TestCase):
    def test_without_configured_credentials_passes_through(self):
        start_response = StartResponse()
        app = BasicAuthMiddleware(ok_app, None, None)

        body = b"".join(app({}, start_response))

        self.assertEqual(start_response.status, "200 OK")
        self.assertEqual(body, b"ok")

    def test_missing_authorization_header_is_rejected(self):
        start_response = StartResponse()
        app = BasicAuthMiddleware(ok_app, "web-user", "web-pass")

        body = b"".join(app({}, start_response))

        self.assertEqual(start_response.status, "401 Unauthorized")
        self.assertEqual(start_response.headers["WWW-Authenticate"], 'Basic realm="webNUT"')
        self.assertEqual(body, b"Unauthorized")

    def test_invalid_credentials_are_rejected(self):
        start_response = StartResponse()
        app = BasicAuthMiddleware(ok_app, "web-user", "web-pass")
        token = base64.b64encode(b"web-user:wrong").decode("ascii")

        body = b"".join(app({"HTTP_AUTHORIZATION": "Basic %s" % token}, start_response))

        self.assertEqual(start_response.status, "401 Unauthorized")
        self.assertEqual(body, b"Unauthorized")

    def test_valid_credentials_pass_through(self):
        start_response = StartResponse()
        app = BasicAuthMiddleware(ok_app, "web-user", "web-pass")
        token = base64.b64encode(b"web-user:web-pass").decode("ascii")

        body = b"".join(app({"HTTP_AUTHORIZATION": "Basic %s" % token}, start_response))

        self.assertEqual(start_response.status, "200 OK")
        self.assertEqual(body, b"ok")
