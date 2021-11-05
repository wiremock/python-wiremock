import responses

from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.client import Scenarios


class ScenariosResourceTests(BaseClientTestCase):
    @attr("unit", "scenarios", "resource")
    @responses.activate
    def test_reset_scenarios(self):
        responses.add(responses.POST, "http://localhost/__admin/scenarios/reset", body="", status=200)

        r = Scenarios.reset_all_scenarios()
        self.assertEqual(200, r.status_code)
