import responses

from tests.utils import assertEqual, assertIsInstance
from wiremock.client import (
    NearMissMatch,
    NearMissMatchPatternRequest,
    NearMissMatchResponse,
    RequestCountResponse,
    RequestResponse,
    RequestResponseAll,
    RequestResponseAllMeta,
    RequestResponseDefinition,
    RequestResponseFindResponse,
    RequestResponseRequest,
    Requests,
)
from wiremock.resources.near_misses import NearMissMatchRequest


@responses.activate
def test_get_all_received_requests():
    e = RequestResponseAll(
        requests=[],
        meta=RequestResponseAllMeta(total=1),
        request_journal_disabled=False,
    )
    resp = e.get_json_data()
    responses.add(
        responses.GET, "http://localhost/__admin/requests", json=resp, status=200
    )

    r = Requests.get_all_received_requests()
    assertIsInstance(r, RequestResponseAll)
    assertEqual(False, r.request_journal_disabled)


@responses.activate
def test_get_request():
    e = RequestResponse(
        id="1234-5678",
        request=RequestResponseRequest(url="test", method="GET"),
        response_definition=RequestResponseDefinition(url="test", method="GET"),
    )
    resp = e.get_json_data()
    responses.add(
        responses.GET,
        "http://localhost/__admin/requests/1234-5678",
        json=resp,
        status=200,
    )

    r = Requests.get_request("1234-5678")
    assertIsInstance(r, RequestResponse)
    assertEqual("test", r.request.url)
    assertEqual("1234-5678", r.id)


@responses.activate
def test_reset_request_journal():
    responses.add(
        responses.DELETE, "http://localhost/__admin/requests", body="", status=200
    )

    r = Requests.reset_request_journal()
    assertEqual(200, r.status_code)


@responses.activate
def test_get_matching_request_count():
    resp = RequestCountResponse(count=4).get_json_data()
    responses.add(
        responses.POST, "http://localhost/__admin/requests/count", json=resp, status=200
    )

    request = NearMissMatchPatternRequest(url="test", method="GET")

    r = Requests.get_matching_request_count(request)
    assertIsInstance(r, RequestCountResponse)
    assertEqual(4, r.count)


@responses.activate
def test_get_matching_requests():
    e = RequestResponseFindResponse(
        requests=[
            RequestResponseRequest(method="GET", url="test"),
        ],
    )
    resp = e.get_json_data()
    responses.add(
        responses.POST, "http://localhost/__admin/requests/find", json=resp, status=200
    )

    request = NearMissMatchPatternRequest(url="test", method="GET")

    r = Requests.get_matching_requests(request)
    assertIsInstance(r, RequestResponseFindResponse)
    assertIsInstance(r.requests, list)
    assertEqual(1, len(r.requests))
    result = r.requests[0]
    assertIsInstance(result, RequestResponseRequest)
    assertEqual("GET", result.method)
    assertEqual("test", result.url)


@responses.activate
def test_get_unmatched_requests():
    e = RequestResponseFindResponse(
        requests=[
            RequestResponseRequest(method="GET", url="test"),
        ],
    )
    resp = e.get_json_data()
    responses.add(
        responses.GET,
        "http://localhost/__admin/requests/unmatched",
        json=resp,
        status=200,
    )

    r = Requests.get_unmatched_requests()
    assertIsInstance(r, RequestResponseFindResponse)
    assertIsInstance(r.requests, list)
    assertEqual(1, len(r.requests))
    result = r.requests[0]
    assertIsInstance(result, RequestResponseRequest)
    assertEqual("GET", result.method)
    assertEqual("test", result.url)


@responses.activate
def test_get_unmatched_requests_near_misses():
    e = NearMissMatchResponse(
        near_misses=[
            NearMissMatch(request=NearMissMatchRequest(url="test", method="GET")),
        ]
    )
    resp = e.get_json_data()
    responses.add(
        responses.GET,
        "http://localhost/__admin/requests/unmatched/near-misses",
        json=resp,
        status=200,
    )

    r = Requests.get_unmatched_requests_near_misses()
    assertIsInstance(r, NearMissMatchResponse)
    result = r.near_misses[0]
    assertIsInstance(result, NearMissMatch)
    assertEqual("test", result.request.url)
    assertEqual("GET", result.request.method)
