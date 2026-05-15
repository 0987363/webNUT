import os
import sys
import types
import unittest
from unittest import mock


class SettingsTests(unittest.TestCase):
    def setUp(self):
        pyramid = types.ModuleType("pyramid")
        pyramid_config = types.ModuleType("pyramid.config")
        pyramid_httpexceptions = types.ModuleType("pyramid.httpexceptions")
        pyramid_config.Configurator = object
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

    def test_loads_defaults_when_config_file_and_environment_are_missing(self):
        from webnut.settings import load_config

        with mock.patch.dict(os.environ, {}, clear=True):
            settings = load_config()

        self.assertEqual(settings.server, "127.0.0.1")
        self.assertEqual(settings.port, 3493)
        self.assertIsNone(settings.username)
        self.assertIsNone(settings.password)
        self.assertIsNone(settings.webnut_username)
        self.assertIsNone(settings.webnut_password)

    def test_environment_values_override_config_file_values(self):
        config = types.ModuleType("webnut.config")
        config.server = "config-nut"
        config.port = 3493
        config.username = "config-user"
        config.password = "config-pass"
        sys.modules["webnut.config"] = config

        from webnut.settings import load_config

        with mock.patch.dict(
            os.environ,
            {
                "NUT_SERVER": "env-nut",
                "NUT_PORT": "3494",
                "NUT_USERNAME": "env-user",
                "NUT_PASSWORD": "env-pass",
                "WEBNUT_USERNAME": "web-user",
                "WEBNUT_PASSWORD": "web-pass",
            },
            clear=True,
        ):
            settings = load_config()

        self.assertEqual(settings.server, "env-nut")
        self.assertEqual(settings.port, 3494)
        self.assertEqual(settings.username, "env-user")
        self.assertEqual(settings.password, "env-pass")
        self.assertEqual(settings.webnut_username, "web-user")
        self.assertEqual(settings.webnut_password, "web-pass")

    def test_empty_environment_values_do_not_override_config_file_values(self):
        config = types.ModuleType("webnut.config")
        config.server = "config-nut"
        config.port = 3493
        config.username = "config-user"
        config.password = "config-pass"
        sys.modules["webnut.config"] = config

        from webnut.settings import load_config

        with mock.patch.dict(
            os.environ,
            {
                "NUT_SERVER": "",
                "NUT_PORT": "",
                "NUT_USERNAME": "",
                "NUT_PASSWORD": "",
            },
            clear=True,
        ):
            settings = load_config()

        self.assertEqual(settings.server, "config-nut")
        self.assertEqual(settings.port, 3493)
        self.assertEqual(settings.username, "config-user")
        self.assertEqual(settings.password, "config-pass")

    def test_webnut_environment_values_do_not_override_nut_credentials(self):
        config = types.ModuleType("webnut.config")
        config.server = "config-nut"
        config.port = 3493
        config.username = "config-user"
        config.password = "config-pass"
        sys.modules["webnut.config"] = config

        from webnut.settings import load_config

        with mock.patch.dict(
            os.environ,
            {
                "WEBNUT_USERNAME": "web-user",
                "WEBNUT_PASSWORD": "web-pass",
            },
            clear=True,
        ):
            settings = load_config()

        self.assertEqual(settings.username, "config-user")
        self.assertEqual(settings.password, "config-pass")
        self.assertEqual(settings.webnut_username, "web-user")
        self.assertEqual(settings.webnut_password, "web-pass")

    def test_webnut_environment_values_override_webnut_config_values(self):
        config = types.ModuleType("webnut.config")
        config.server = "config-nut"
        config.port = 3493
        config.username = None
        config.password = None
        config.webnut_username = "config-web-user"
        config.webnut_password = "config-web-pass"
        sys.modules["webnut.config"] = config

        from webnut.settings import load_config

        with mock.patch.dict(
            os.environ,
            {
                "WEBNUT_USERNAME": "env-web-user",
                "WEBNUT_PASSWORD": "env-web-pass",
            },
            clear=True,
        ):
            settings = load_config()

        self.assertEqual(settings.webnut_username, "env-web-user")
        self.assertEqual(settings.webnut_password, "env-web-pass")

    def test_invalid_environment_port_does_not_override_config_file_value(self):
        config = types.ModuleType("webnut.config")
        config.server = "config-nut"
        config.port = 3493
        config.username = None
        config.password = None
        sys.modules["webnut.config"] = config

        from webnut.settings import load_config

        with mock.patch.dict(os.environ, {"NUT_PORT": "invalid"}, clear=True):
            settings = load_config()

        self.assertEqual(settings.port, 3493)
