import pytest
from wiremock.tests.base import BaseClientTestCase
from wiremock.resources.settings import GlobalSetting


class SettingsSerializationTests(BaseClientTestCase):
    @pytest.mark.unit
    @pytest.mark.serialization
    @pytest.mark.settings
    def test_global_settings_serialization(self):
        gs = GlobalSetting(fixed_delay=500)
        serialized = gs.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "fixedDelay", 500)

    @pytest.mark.unit
    @pytest.mark.serialization
    @pytest.mark.settings
    def test_global_settings_deserialization(self):
        serialized = {"fixedDelay": 500}
        gs = GlobalSetting.from_dict(serialized)
        self.assertIsInstance(gs, GlobalSetting)
        self.assertEqual(500, gs.fixed_delay)
