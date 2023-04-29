import responses

from tests.utils import assertEqual
from wiremock.client import Scenarios


@responses.activate
def test_reset_scenarios():
    responses.add(
        responses.POST,
        "http://localhost/__admin/scenarios/reset",
        body="",
        status=200,
    )

    r = Scenarios.reset_all_scenarios()
    assertEqual(200, r.status_code)
