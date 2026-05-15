from pathlib import Path
import unittest


class ReverseProxyLinkTests(unittest.TestCase):
    def test_ups_links_use_same_origin_paths(self):
        template = Path("webnut/templates/index.pt").read_text()

        self.assertIn("request.route_path('ups_view', ups=ups)", template)
        self.assertNotIn("request.route_url('ups_view', ups=ups)", template)
