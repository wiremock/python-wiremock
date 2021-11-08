import responses

from wiremock.resources.near_misses import NearMissMatchRequest
from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.client import (
    RequestResponseDefinition,
    RequestResponseRequest,
    RequestResponse,
    RequestCountResponse,
    RequestResponseAll,
    RequestResponseFindResponse,
    Requests,
    RequestResponseAllMeta,
    NearMissMatchPatternRequest,
    NearMissMatchResponse,
    NearMissMatch,
)


class RequestsResourceTests(BaseClientTestCase):
    @attr("unit", "requests", "resource")
    @responses.activate
    def test_get_all_received_requests(self):
        e = RequestResponseAll(requests=[], meta=RequestResponseAllMeta(total=1), request_journal_disabled=False)
        resp = e.get_json_data()
        responses.add(responses.GET, "http://localhost/__admin/requests", json=resp, status=200)

        r = Requests.get_all_received_requests()
        self.assertIsInstance(r, RequestResponseAll)
        self.assertEqual(False, r.request_journal_disabled)

    @attr("unit", "requests", "resource")
    @responses.activate
    def test_get_request(self):
        e = RequestResponse(
            id="1234-5678",
            request=RequestResponseRequest(url="test", method="GET"),
            response_definition=RequestResponseDefinition(url="test", method="GET"),
        )
        resp = e.get_json_data()
        responses.add(responses.GET, "http://localhost/__admin/requests/1234-5678", json=resp, status=200)

        r = Requests.get_request("1234-5678")
        self.assertIsInstance(r, RequestResponse)
        self.assertEqual("test", r.request.url)
        self.assertEqual("1234-5678", r.id)

    @attr("unit", "requests", "resource")
    @responses.activate
    def test_reset_request_journal(self):
        responses.add(responses.POST, "http://localhost/__admin/requests/reset", body="", status=200)

        r = Requests.reset_request_journal()
        self.assertEqual(200, r.status_code)

    @attr("unit", "requests", "resource")
    @responses.activate
    def test_get_matching_request_count(self):
        resp = RequestCountResponse(count=4).get_json_data()
        responses.add(responses.POST, "http://localhost/__admin/requests/count", json=resp, status=200)

        request = NearMissMatchPatternRequest(url="test", method="GET")

        r = Requests.get_matching_request_count(request)
        self.assertIsInstance(r, RequestCountResponse)
        self.assertEqual(4, r.count)

    @attr("unit", "requests", "resource")
    @responses.activate
    def test_get_matching_requests(self):
        e = RequestResponseFindResponse(requests=[RequestResponseRequest(method="GET", url="test"),],)
        resp = e.get_json_data()
        responses.add(responses.POST, "http://localhost/__admin/requests/find", json=resp, status=200)

        request = NearMissMatchPatternRequest(url="test", method="GET")

        r = Requests.get_matching_requests(request)
        self.assertIsInstance(r, RequestResponseFindResponse)
        self.assertIsInstance(r.requests, list)
        self.assertEqual(1, len(r.requests))
        result = r.requests[0]
        self.assertIsInstance(result, RequestResponseRequest)
        self.assertEqual("GET", result.method)
        self.assertEqual("test", result.url)

    @attr("unit", "requests", "resource")
    @responses.activate
    def test_get_unmatched_requests(self):
        e = RequestResponseFindResponse(requests=[RequestResponseRequest(method="GET", url="test"),],)
        resp = e.get_json_data()
        responses.add(responses.GET, "http://localhost/__admin/requests/unmatched", json=resp, status=200)

        r = Requests.get_unmatched_requests()
        self.assertIsInstance(r, RequestResponseFindResponse)
        self.assertIsInstance(r.requests, list)
        self.assertEqual(1, len(r.requests))
        result = r.requests[0]
        self.assertIsInstance(result, RequestResponseRequest)
        self.assertEqual("GET", result.method)
        self.assertEqual("test", result.url)

    @attr("unit", "requests", "resource")
    @responses.activate
    def test_get_unmatched_requests_near_misses(self):
        e = NearMissMatchResponse(near_misses=[NearMissMatch(request=NearMissMatchRequest(url="test", method="GET")),])
        resp = e.get_json_data()
        responses.add(responses.GET, "http://localhost/__admin/requests/unmatched/near-misses", json=resp, status=200)

        r = Requests.get_unmatched_requests_near_misses()
        self.assertIsInstance(r, NearMissMatchResponse)
        result = r.near_misses[0]
        self.assertIsInstance(result, NearMissMatch)
        self.assertEqual("test", result.request.url)
        self.assertEqual("GET", result.request.method)
