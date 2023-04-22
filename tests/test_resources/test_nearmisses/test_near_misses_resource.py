import pytest
import responses

from wiremock.client import (
    NearMisses,
    NearMissMatch,
    NearMissMatchPatternRequest,
    NearMissMatchRequest,
    NearMissMatchResponse,
    NearMissMatchResult,
    NearMissRequestPatternResult,
)
from wiremock.resources.mappings import HttpMethods


@pytest.mark.unit
@pytest.mark.resource
@pytest.mark.nearmisses
@responses.activate
def test_find_nearest_misses_by_request():
    e = NearMissMatchResponse(
        near_misses=[
            NearMissMatch(
                request=NearMissMatchRequest(url="test", method="GET"),
                request_pattern=NearMissRequestPatternResult(
                    url="test1",
                    method="GET",
                ),
                match_result=NearMissMatchResult(distance=0.5),
            ),
        ]
    )
    resp = e.get_json_data()
    responses.add(
        responses.POST,
        "http://localhost/__admin/near-misses/request",
        json=resp,
        status=200,
    )

    near_miss_match_request = NearMissMatchRequest(
        url="test",
        method=HttpMethods.GET,
    )
    r = NearMisses.find_nearest_misses_by_request(near_miss_match_request)
    assert isinstance(r, NearMissMatchResponse)
    assert isinstance(r.near_misses, list)
    result = r.near_misses[0]
    assert isinstance(result, NearMissMatch)
    assert result.request.url == "test"


@pytest.mark.unit
@pytest.mark.resource
@pytest.mark.nearmisses
@responses.activate
def test_find_nearest_misses_by_request_pattern():
    e = NearMissMatchResponse(
        near_misses=[
            NearMissMatch(
                request=NearMissMatchRequest(url="test", method="GET"),
                request_pattern=NearMissRequestPatternResult(
                    url="test1",
                    method="GET",
                ),
                match_result=NearMissMatchResult(distance=0.5),
            ),
        ]
    )
    resp = e.get_json_data()
    responses.add(
        responses.POST,
        "http://localhost/__admin/near-misses/request-pattern",
        json=resp,
        status=200,
    )

    near_miss_match_request_pattern = NearMissMatchPatternRequest(
        url="test", method=HttpMethods.GET
    )
    r = NearMisses.find_nearest_misses_by_request_pattern(
        near_miss_match_request_pattern
    )
    assert isinstance(r, NearMissMatchResponse)
    assert isinstance(r.near_misses, list)
    result = r.near_misses[0]
    assert isinstance(result, NearMissMatch)
    assert result.request.url == "test"
