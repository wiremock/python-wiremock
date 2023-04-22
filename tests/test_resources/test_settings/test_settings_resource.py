import responses

from tests.utils import assertEqual, assertIsInstance
from wiremock.client import GlobalSetting, GlobalSettings


@responses.activate
def test_update_settings():
    e = GlobalSetting(fixed_delay=500)
    resp = e.get_json_data()
    responses.add(
        responses.POST, "http://localhost/__admin/settings", json=resp, status=200
    )

    r = GlobalSettings.update_global_settings(e)
    assertIsInstance(r, GlobalSetting)
    assertEqual(500, r.fixed_delay)
