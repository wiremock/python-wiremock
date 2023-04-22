import pytest

from tests.utils import (
    assertDictContainsKeyWithValue,
    assertDictContainsKeyWithValueType,
)
from wiremock.resources.mappings import BasicAuthCredentials, CommonHeaders, HttpMethods
from wiremock.resources.near_misses import (
    NearMissMatch,
    NearMissMatchPatternRequest,
    NearMissMatchRequest,
    NearMissMatchResponse,
    NearMissMatchResult,
    NearMissRequestPatternResult,
)


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_pattern_request_serialization():
    e = NearMissMatchPatternRequest(
        url="test",
        url_pattern="test2",
        url_path="test3",
        url_path_pattern="test4",
        method=HttpMethods.GET,
        client_ip="1.1.1.1",
        headers={CommonHeaders.ACCEPT: "json"},
        query_parameters={"test": 1},
        cookies={"chocolate": "chip"},
        body_patterns={"test": 3},
        basic_auth_credentials=BasicAuthCredentials(
            username="username", password="password"
        ),
        browser_proxy_request=False,
        logged_date=12345,
        logged_date_string="1/1/2017 00:00:00+0000",
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "url", "test")
    assertDictContainsKeyWithValue(serialized, "urlPattern", "test2")
    assertDictContainsKeyWithValue(serialized, "urlPath", "test3")
    assertDictContainsKeyWithValue(serialized, "urlPathPattern", "test4")
    assertDictContainsKeyWithValue(serialized, "method", "GET")
    assertDictContainsKeyWithValue(serialized, "clientIp", "1.1.1.1")
    assertDictContainsKeyWithValue(serialized, "headers", {"Accept": "json"})
    assertDictContainsKeyWithValue(serialized, "queryParameters", {"test": 1})
    assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
    assertDictContainsKeyWithValue(serialized, "bodyPatterns", {"test": 3})
    assertDictContainsKeyWithValue(
        serialized,
        "basicAuthCredentials",
        {"username": "username", "password": "password"},
    )
    assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
    assertDictContainsKeyWithValue(serialized, "loggedDate", 12345)
    assertDictContainsKeyWithValue(
        serialized, "loggedDateString", "1/1/2017 00:00:00+0000"
    )


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_pattern_request_deserialization():
    serialized = {
        "clientIp": "1.1.1.1",
        "cookies": {"chocolate": "chip"},
        "loggedDate": 12345,
        "urlPattern": "test2",
        "headers": {"Accept": "json"},
        "url": "test",
        "urlPath": "test3",
        "urlPathPattern": "test4",
        "browserProxyRequest": False,
        "loggedDateString": "1/1/2017 00:00:00+0000",
        "bodyPatterns": {"test": 3},
        "queryParameters": {"test": 1},
        "basicAuthCredentials": {"username": "username", "password": "password"},
        "method": "GET",
    }
    e = NearMissMatchPatternRequest.from_dict(serialized)
    assert isinstance(e, NearMissMatchPatternRequest)
    assert e.url == "test"
    assert e.url_pattern == "test2"
    assert e.url_path == "test3"
    assert e.url_path_pattern == "test4"
    assert e.method == "GET"
    assert e.client_ip == "1.1.1.1"
    assert e.headers == {"Accept": "json"}
    assert e.query_parameters == {"test": 1}
    assert e.cookies == {"chocolate": "chip"}
    assertDictContainsKeyWithValue(e.body_patterns, "test", 3)
    assert isinstance(e.basic_auth_credentials, BasicAuthCredentials)
    assert e.basic_auth_credentials.username == "username"
    assert e.basic_auth_credentials.password == "password"
    assert e.browser_proxy_request == False
    assert e.logged_date == 12345
    assert e.logged_date_string == "1/1/2017 00:00:00+0000"


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_request_serialization():
    e = NearMissMatchRequest(
        url="test",
        absolute_url="test2",
        method=HttpMethods.GET,
        client_ip="1.1.1.1",
        headers={CommonHeaders.ACCEPT: "json"},
        query_parameters={"test": 1},
        cookies={"chocolate": "chip"},
        basic_auth_credentials=BasicAuthCredentials(
            username="username", password="password"
        ),
        browser_proxy_request=False,
        logged_date=12345,
        logged_date_string="1/1/2017 00:00:00+0000",
        body_as_base64="test3",
        body="test4",
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "url", "test")
    assertDictContainsKeyWithValue(serialized, "absoluteUrl", "test2")
    assertDictContainsKeyWithValue(serialized, "method", HttpMethods.GET)
    assertDictContainsKeyWithValue(serialized, "clientIp", "1.1.1.1")
    assertDictContainsKeyWithValue(
        serialized, "headers", {CommonHeaders.ACCEPT: "json"}
    )
    assertDictContainsKeyWithValue(serialized, "queryParameters", {"test": 1})
    assertDictContainsKeyWithValue(
        serialized,
        "cookies",
        {
            "chocolate": "chip",
        },
    )
    assertDictContainsKeyWithValue(
        serialized,
        "basicAuthCredentials",
        {"username": "username", "password": "password"},
    )
    assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
    assertDictContainsKeyWithValue(serialized, "loggedDate", 12345)
    assertDictContainsKeyWithValue(
        serialized, "loggedDateString", "1/1/2017 00:00:00+0000"
    )
    assertDictContainsKeyWithValue(serialized, "bodyAsBase64", "test3")
    assertDictContainsKeyWithValue(serialized, "body", "test4")


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_request_deserialization():
    serialized = {
        "clientIp": "1.1.1.1",
        "cookies": {"chocolate": "chip"},
        "loggedDate": 12345,
        "absoluteUrl": "test2",
        "headers": {"Accept": "json"},
        "url": "test",
        "browserProxyRequest": False,
        "body": "test4",
        "bodyAsBase64": "test3",
        "loggedDateString": "1/1/2017 00:00:00+0000",
        "queryParameters": {"test": 1},
        "basicAuthCredentials": {"username": "username", "password": "password"},
        "method": "GET",
    }
    e = NearMissMatchRequest.from_dict(serialized)
    assert isinstance(e, NearMissMatchRequest)
    assert e.url == "test"
    assert e.absolute_url == "test2"
    assert e.method == "GET"
    assert e.client_ip == "1.1.1.1"
    assertDictContainsKeyWithValue(e.headers, "Accept", "json")
    assertDictContainsKeyWithValue(e.query_parameters, "test", 1)
    assertDictContainsKeyWithValue(e.cookies, "chocolate", "chip")
    assert isinstance(e.basic_auth_credentials, BasicAuthCredentials)
    assert e.basic_auth_credentials.username == "username"
    assert e.basic_auth_credentials.password == "password"
    assert e.browser_proxy_request == False
    assert e.logged_date == 12345
    assert e.logged_date_string == "1/1/2017 00:00:00+0000"
    assert e.body_as_base64 == "test3"
    assert e.body == "test4"


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_result_deserialization():
    serialized = {"distance": 0.75}
    e = NearMissMatchResult.from_dict(serialized)
    assert isinstance(e, NearMissMatchResult)
    assert e.distance == 0.75


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_request_pattern_result_serialization():
    e = NearMissRequestPatternResult(
        url="test",
        absolute_url="test2",
        method=HttpMethods.GET,
        client_ip="1.1.1.1",
        headers={CommonHeaders.ACCEPT: "json"},
        query_parameters={"test": 1},
        cookies={"chocolate": "chip"},
        basic_auth_credentials=BasicAuthCredentials(
            username="username", password="password"
        ),
        browser_proxy_request=False,
        body_as_base64="test3",
        body="test4",
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "url", "test")
    assertDictContainsKeyWithValue(serialized, "absoluteUrl", "test2")
    assertDictContainsKeyWithValue(serialized, "method", "GET")
    assertDictContainsKeyWithValue(serialized, "clientIp", "1.1.1.1")
    assertDictContainsKeyWithValue(serialized, "headers", {"Accept": "json"})
    assertDictContainsKeyWithValue(serialized, "queryParameters", {"test": 1})
    assertDictContainsKeyWithValue(
        serialized,
        "cookies",
        {
            "chocolate": "chip",
        },
    )
    assertDictContainsKeyWithValue(
        serialized,
        "basicAuthCredentials",
        {"username": "username", "password": "password"},
    )
    assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
    assertDictContainsKeyWithValue(serialized, "bodyAsBase64", "test3")
    assertDictContainsKeyWithValue(serialized, "body", "test4")


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_request_pattern_result_deserialization():
    serialized = {
        "clientIp": "1.1.1.1",
        "cookies": {"chocolate": "chip"},
        "absoluteUrl": "test2",
        "headers": {"Accept": "json"},
        "url": "test",
        "browserProxyRequest": False,
        "body": "test4",
        "bodyAsBase64": "test3",
        "queryParameters": {"test": 1},
        "basicAuthCredentials": {
            "username": "username",
            "password": "password",
        },
        "method": "GET",
    }
    e = NearMissRequestPatternResult.from_dict(serialized)
    assert isinstance(e, NearMissRequestPatternResult)
    assert "test" == e.url
    assert "test2" == e.absolute_url
    assert "GET" == e.method
    assert "1.1.1.1" == e.client_ip
    assert {"Accept": "json"} == e.headers
    assert {"test": 1} == e.query_parameters
    assert {"chocolate": "chip"} == e.cookies
    assert isinstance(e.basic_auth_credentials, BasicAuthCredentials)
    assert "username" == e.basic_auth_credentials.username
    assert "password" == e.basic_auth_credentials.password
    assert False is e.browser_proxy_request
    assert e.body_as_base64 == "test3"
    assert e.body == "test4"


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_serialization():
    e = NearMissMatch(
        request=NearMissMatchRequest(url="test"),
        request_pattern=NearMissRequestPatternResult(url="test2"),
        match_result=NearMissMatchResult(distance=0.75),
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValueType(serialized, "request", dict)
    request = serialized["request"]
    assertDictContainsKeyWithValue(request, "url", "test")

    assertDictContainsKeyWithValueType(serialized, "requestPattern", dict)
    request_pattern = serialized["requestPattern"]
    assertDictContainsKeyWithValue(request_pattern, "url", "test2")

    assertDictContainsKeyWithValueType(serialized, "matchResult", dict)
    match_result = serialized["matchResult"]
    assertDictContainsKeyWithValue(match_result, "distance", 0.75)


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.nearmisses
def test_near_miss_match_deserialization():
    serialized = {
        "request": {
            "clientIp": "1.1.1.1",
            "cookies": {"chocolate": "chip"},
            "loggedDate": 12345,
            "absoluteUrl": "test2",
            "headers": {"Accept": "json"},
            "url": "test",
            "browserProxyRequest": False,
            "body": "test4",
            "bodyAsBase64": "test3",
            "loggedDateString": "1/1/2017 00:00:00+0000",
            "queryParameters": {"test": 1},
            "basicAuthCredentials": {
                "username": "username",
                "password": "password",
            },
            "method": "GET",
        },
        "requestPattern": {
            "clientIp": "1.1.1.1",
            "cookies": {"chocolate": "chip"},
            "absoluteUrl": "test2",
            "headers": {"Accept": "json"},
            "url": "test",
            "browserProxyRequest": False,
            "body": "test4",
            "bodyAsBase64": "test3",
            "queryParameters": {"test": 1},
            "basicAuthCredentials": {
                "username": "username",
                "password": "password",
            },
            "method": "GET",
        },
        "matchResult": {"distance": 0.75},
    }
    e = NearMissMatch.from_dict(serialized)
    assert isinstance(e, NearMissMatch)
    assert isinstance(e.request, NearMissMatchRequest)
    assert isinstance(e.request_pattern, NearMissRequestPatternResult)
    assert isinstance(e.match_result, NearMissMatchResult)

    # request
    _request = serialized["request"]
    assertDictContainsKeyWithValue(_request, "url", "test")
    assertDictContainsKeyWithValue(_request, "absoluteUrl", "test2")
    assertDictContainsKeyWithValue(_request, "method", "GET")
    assertDictContainsKeyWithValue(_request, "clientIp", "1.1.1.1")
    assertDictContainsKeyWithValue(_request, "headers", {"Accept": "json"})
    assertDictContainsKeyWithValue(_request, "queryParameters", {"test": 1})
    assertDictContainsKeyWithValue(_request, "cookies", {"chocolate": "chip"})
    assertDictContainsKeyWithValue(_request, "bodyAsBase64", "test3")
    assertDictContainsKeyWithValue(_request, "body", "test4")
    assertDictContainsKeyWithValue(_request, "loggedDate", 12345)
    assertDictContainsKeyWithValue(
        _request, "loggedDateString", "1/1/2017 00:00:00+0000"
    )

    _basicAuth = serialized["request"]["basicAuthCredentials"]
    assertDictContainsKeyWithValueType(
        serialized["request"], "basicAuthCredentials", dict
    )
    assertDictContainsKeyWithValue(_basicAuth, "username", "username")
    assertDictContainsKeyWithValue(_basicAuth, "password", "password")
    assertDictContainsKeyWithValue(serialized["request"], "browserProxyRequest", False)

    # request pattern
    _requestPattern = serialized["requestPattern"]
    assertDictContainsKeyWithValue(_requestPattern, "url", "test")
    assertDictContainsKeyWithValue(_requestPattern, "absoluteUrl", "test2")
    assertDictContainsKeyWithValue(_requestPattern, "method", "GET")
    assertDictContainsKeyWithValue(_requestPattern, "clientIp", "1.1.1.1")
    assertDictContainsKeyWithValue(_requestPattern, "headers", {"Accept": "json"})
    assertDictContainsKeyWithValue(_requestPattern, "queryParameters", {"test": 1})
    assertDictContainsKeyWithValue(_requestPattern, "cookies", {"chocolate": "chip"})
    assertDictContainsKeyWithValue(_requestPattern, "bodyAsBase64", "test3")
    assertDictContainsKeyWithValue(_requestPattern, "body", "test4")

    _basicAuth = serialized["requestPattern"]["basicAuthCredentials"]
    assertDictContainsKeyWithValueType(
        serialized["requestPattern"], "basicAuthCredentials", dict
    )
    assertDictContainsKeyWithValue(_basicAuth, "username", "username")
    assertDictContainsKeyWithValue(_basicAuth, "password", "password")
    assertDictContainsKeyWithValue(
        serialized["requestPattern"], "browserProxyRequest", False
    )
    # match result
    assertDictContainsKeyWithValue(serialized["matchResult"], "distance", 0.75)


def test_near_miss_match_response_serialization():
    e = NearMissMatchResponse(
        near_misses=[
            NearMissMatch(
                request=NearMissMatchRequest(url="test"),
                request_pattern=NearMissRequestPatternResult(url="test2"),
                match_result=NearMissMatchResult(distance=0.75),
            )
        ]
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValueType(serialized, "nearMisses", list)
    near_miss = serialized["nearMisses"][0]
    assertDictContainsKeyWithValueType(near_miss, "request", dict)
    assertDictContainsKeyWithValue(near_miss["request"], "url", "test")
    assertDictContainsKeyWithValueType(near_miss, "requestPattern", dict)
    assertDictContainsKeyWithValue(near_miss["requestPattern"], "url", "test2")
    assertDictContainsKeyWithValueType(near_miss, "matchResult", dict)
    assertDictContainsKeyWithValue(near_miss["matchResult"], "distance", 0.75)


def test_near_miss_match_response_deserialization():
    serialized = {
        "nearMisses": [
            {
                "request": {"url": "test"},
                "requestPattern": {"url": "test"},
                "matchResult": {"distance": 0.75},
            }
        ]
    }
    e = NearMissMatchResponse.from_dict(serialized)
    assert isinstance(e, NearMissMatchResponse)
    assert isinstance(e.near_misses, list)
    assert len(e.near_misses) == 1
    near_miss = e.near_misses[0]
    assert isinstance(near_miss, NearMissMatch)
    assert isinstance(near_miss.request, NearMissMatchRequest)
    assert isinstance(near_miss.request_pattern, NearMissRequestPatternResult)
    assert isinstance(near_miss.match_result, NearMissMatchResult)
