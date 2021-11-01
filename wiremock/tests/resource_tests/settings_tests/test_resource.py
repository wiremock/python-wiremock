import responses
import pytest

from wiremock.tests.base import BaseClientTestCase
from wiremock.client import GlobalSetting, GlobalSettings


class SettingsResourceTests(BaseClientTestCase):
    @pytest.mark.unit
    @pytest.mark.settings
    @pytest.mark.resource
    @responses.activate
    def test_update_settings(self):
        e = GlobalSetting(fixed_delay=500)
        resp = e.get_json_data()
        responses.add(
            responses.POST, "http://localhost/__admin/settings", json=resp, status=200
        )

        r = GlobalSettings.update_global_settings(e)
        self.assertIsInstance(r, GlobalSetting)
        self.assertEqual(500, r.fixed_delay)
