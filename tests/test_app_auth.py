import os
import sys
import types
import unittest
from unittest import mock


class ConfiguratorStub(object):
    def __init__(self, settings=None):
        self.settings = settings

    def include(self, name):
        pass

    def add_static_view(self, *args, **kwargs):
        pass

    def add_route(self, *args, **kwargs):
        pass

    def add_view(self, *args, **kwargs):
        pass

    def scan(self):
        pass

    def make_wsgi_app(self):
        def app(environ, start_response):
            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"ok"]

        return app


class StartResponse(object):
    def __call__(self, status, headers):
        self.status = status
        self.headers = dict(headers)


class AppAuthTests(unittest.TestCase):
    def setUp(self):
        pyramid = types.ModuleType("pyramid")
        pyramid_config = types.ModuleType("pyramid.config")
        pyramid_httpexceptions = types.ModuleType("pyramid.httpexceptions")
        pyramid_config.Configurator = ConfiguratorStub
        pyramid_httpexceptions.HTTPNotFound = object
        self.pyramid_patch = mock.patch.dict(
            sys.modules,
            {
                "pyramid": pyramid,
                "pyramid.config": pyramid_config,
                "pyramid.httpexceptions": pyramid_httpexceptions,
            },
        )
        self.pyramid_patch.start()

    def tearDown(self):
        self.pyramid_patch.stop()
        sys.modules.pop("webnut", None)
        sys.modules.pop("webnut.settings", None)
        sys.modules.pop("webnut.config", None)
        sys.modules.pop("webnut.basic_auth", None)

    def test_main_app_requires_basic_auth_when_webnut_credentials_are_set(self):
        with mock.patch.dict(
            os.environ,
            {
                "WEBNUT_USERNAME": "web-user",
                "WEBNUT_PASSWORD": "web-pass",
            },
            clear=True,
        ):
            import webnut

            app = webnut.main({})

        start_response = StartResponse()
        body = b"".join(app({}, start_response))

        self.assertEqual(start_response.status, "401 Unauthorized")
        self.assertEqual(body, b"Unauthorized")
