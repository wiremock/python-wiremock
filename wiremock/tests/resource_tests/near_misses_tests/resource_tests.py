import responses

from wiremock.resources.mappings import HttpMethods
from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.client import (
    NearMisses,
    NearMissMatch,
    NearMissMatchPatternRequest,
    NearMissMatchRequest,
    NearMissMatchResponse,
    NearMissMatchResult,
    NearMissRequestPatternResult,
)


class NearMissesResourceTests(BaseClientTestCase):
    @attr("unit", "nearmisses", "resource")
    @responses.activate
    def test_find_nearest_misses_by_request(self):
        e = NearMissMatchResponse(
            near_misses=[
                NearMissMatch(
                    request=NearMissMatchRequest(url="test", method="GET"),
                    request_pattern=NearMissRequestPatternResult(url="test1", method="GET"),
                    match_result=NearMissMatchResult(distance=0.5),
                ),
            ]
        )
        resp = e.get_json_data()
        responses.add(responses.POST, "http://localhost/__admin/near-misses/request", json=resp, status=200)

        near_miss_match_request = NearMissMatchRequest(url="test", method=HttpMethods.GET)
        r = NearMisses.find_nearest_misses_by_request(near_miss_match_request)
        self.assertIsInstance(r, NearMissMatchResponse)
        self.assertIsInstance(r.near_misses, list)
        result = r.near_misses[0]
        self.assertIsInstance(result, NearMissMatch)
        self.assertEqual("test", result.request.url)

    @attr("unit", "nearmisses", "resource")
    @responses.activate
    def test_find_nearest_misses_by_request_pattern(self):
        e = NearMissMatchResponse(
            near_misses=[
                NearMissMatch(
                    request=NearMissMatchRequest(url="test", method="GET"),
                    request_pattern=NearMissRequestPatternResult(url="test1", method="GET"),
                    match_result=NearMissMatchResult(distance=0.5),
                ),
            ]
        )
        resp = e.get_json_data()
        responses.add(responses.POST, "http://localhost/__admin/near-misses/request-pattern", json=resp, status=200)

        near_miss_match_request_pattern = NearMissMatchPatternRequest(url="test", method=HttpMethods.GET)
        r = NearMisses.find_nearest_misses_by_request_pattern(near_miss_match_request_pattern)
        self.assertIsInstance(r, NearMissMatchResponse)
        self.assertIsInstance(r.near_misses, list)
        result = r.near_misses[0]
        self.assertIsInstance(result, NearMissMatch)
        self.assertEqual("test", result.request.url)
