from tests.utils import assertDictContainsKeyWithValue, assertEqual, assertIsInstance
from wiremock.resources.settings import GlobalSetting


def test_global_settings_serialization():
    gs = GlobalSetting(fixed_delay=500)
    serialized = gs.get_json_data()
    assertDictContainsKeyWithValue(serialized, "fixedDelay", 500)


def test_global_settings_deserialization():
    serialized = {"fixedDelay": 500}
    gs = GlobalSetting.from_dict(serialized)
    assertIsInstance(gs, GlobalSetting)
    assertEqual(500, gs.fixed_delay)
