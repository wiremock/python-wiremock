from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.resources.mappings import HttpMethods, CommonHeaders, BasicAuthCredentials
from wiremock.resources.near_misses import (
    NearMissMatchPatternRequest,
    NearMissMatchResponse,
    NearMissMatchRequest,
    NearMissMatch,
    NearMissMatchResult,
    NearMissRequestPatternResult,
)


class NearMissesSerializationTests(BaseClientTestCase):
    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_pattern_request_serialization(self):
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
            basic_auth_credentials=BasicAuthCredentials(username="username", password="password"),
            browser_proxy_request=False,
            logged_date=12345,
            logged_date_string="1/1/2017 00:00:00+0000",
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "url", "test")
        self.assertDictContainsKeyWithValue(serialized, "urlPattern", "test2")
        self.assertDictContainsKeyWithValue(serialized, "urlPath", "test3")
        self.assertDictContainsKeyWithValue(serialized, "urlPathPattern", "test4")
        self.assertDictContainsKeyWithValue(serialized, "method", "GET")
        self.assertDictContainsKeyWithValue(serialized, "clientIp", "1.1.1.1")
        self.assertDictContainsKeyWithValue(serialized, "headers", {"Accept": "json"})
        self.assertDictContainsKeyWithValue(serialized, "queryParameters", {"test": 1})
        self.assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
        self.assertDictContainsKeyWithValue(serialized, "bodyPatterns", {"test": 3})
        self.assertDictContainsKeyWithValue(serialized, "basicAuthCredentials", {"username": "username", "password": "password"})
        self.assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
        self.assertDictContainsKeyWithValue(serialized, "loggedDate", 12345)
        self.assertDictContainsKeyWithValue(serialized, "loggedDateString", "1/1/2017 00:00:00+0000")

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_pattern_request_deserialization(self):
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
        self.assertIsInstance(e, NearMissMatchPatternRequest)
        self.assertEqual("test", e.url)
        self.assertEqual("test2", e.url_pattern)
        self.assertEqual("test3", e.url_path)
        self.assertEqual("test4", e.url_path_pattern)
        self.assertEqual("GET", e.method)
        self.assertEqual("1.1.1.1", e.client_ip)
        self.assertEqual({"Accept": "json"}, e.headers)
        self.assertEqual({"test": 1}, e.query_parameters)
        self.assertEqual({"chocolate": "chip"}, e.cookies)
        self.assertDictEqual({"test": 3}, e.body_patterns)
        self.assertIsInstance(e.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.basic_auth_credentials.username)
        self.assertEqual("password", e.basic_auth_credentials.password)
        self.assertEqual(False, e.browser_proxy_request)
        self.assertEqual(12345, e.logged_date)
        self.assertEqual("1/1/2017 00:00:00+0000", e.logged_date_string)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_request_serialization(self):
        e = NearMissMatchRequest(
            url="test",
            absolute_url="test2",
            method=HttpMethods.GET,
            client_ip="1.1.1.1",
            headers={CommonHeaders.ACCEPT: "json"},
            query_parameters={"test": 1},
            cookies={"chocolate": "chip"},
            basic_auth_credentials=BasicAuthCredentials(username="username", password="password"),
            browser_proxy_request=False,
            logged_date=12345,
            logged_date_string="1/1/2017 00:00:00+0000",
            body_as_base64="test3",
            body="test4",
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "url", "test")
        self.assertDictContainsKeyWithValue(serialized, "absoluteUrl", "test2")
        self.assertDictContainsKeyWithValue(serialized, "method", "GET")
        self.assertDictContainsKeyWithValue(serialized, "clientIp", "1.1.1.1")
        self.assertDictContainsKeyWithValue(serialized, "headers", {"Accept": "json"})
        self.assertDictContainsKeyWithValue(serialized, "queryParameters", {"test": 1})
        self.assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
        self.assertDictContainsKeyWithValue(serialized, "basicAuthCredentials", {"username": "username", "password": "password"})
        self.assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
        self.assertDictContainsKeyWithValue(serialized, "loggedDate", 12345)
        self.assertDictContainsKeyWithValue(serialized, "loggedDateString", "1/1/2017 00:00:00+0000")
        self.assertDictContainsKeyWithValue(serialized, "bodyAsBase64", "test3")
        self.assertDictContainsKeyWithValue(serialized, "body", "test4")

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_request_deserialization(self):
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
        self.assertIsInstance(e, NearMissMatchRequest)
        self.assertEqual("test", e.url)
        self.assertEqual("test2", e.absolute_url)
        self.assertEqual("GET", e.method)
        self.assertEqual("1.1.1.1", e.client_ip)
        self.assertEqual({"Accept": "json"}, e.headers)
        self.assertEqual({"test": 1}, e.query_parameters)
        self.assertEqual({"chocolate": "chip"}, e.cookies)
        self.assertIsInstance(e.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.basic_auth_credentials.username)
        self.assertEqual("password", e.basic_auth_credentials.password)
        self.assertEqual(False, e.browser_proxy_request)
        self.assertEqual(12345, e.logged_date)
        self.assertEqual("1/1/2017 00:00:00+0000", e.logged_date_string)
        self.assertEqual("test3", e.body_as_base64)
        self.assertEqual("test4", e.body)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_result_serialization(self):
        e = NearMissMatchResult(distance=0.75)
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "distance", 0.75)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_result_deserialization(self):
        serialized = {"distance": 0.75}
        e = NearMissMatchResult.from_dict(serialized)
        self.assertIsInstance(e, NearMissMatchResult)
        self.assertEqual(0.75, e.distance)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_request_pattern_result_serialization(self):
        e = NearMissRequestPatternResult(
            url="test",
            absolute_url="test2",
            method=HttpMethods.GET,
            client_ip="1.1.1.1",
            headers={CommonHeaders.ACCEPT: "json"},
            query_parameters={"test": 1},
            cookies={"chocolate": "chip"},
            basic_auth_credentials=BasicAuthCredentials(username="username", password="password"),
            browser_proxy_request=False,
            body_as_base64="test3",
            body="test4",
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "url", "test")
        self.assertDictContainsKeyWithValue(serialized, "absoluteUrl", "test2")
        self.assertDictContainsKeyWithValue(serialized, "method", "GET")
        self.assertDictContainsKeyWithValue(serialized, "clientIp", "1.1.1.1")
        self.assertDictContainsKeyWithValue(serialized, "headers", {"Accept": "json"})
        self.assertDictContainsKeyWithValue(serialized, "queryParameters", {"test": 1})
        self.assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
        self.assertDictContainsKeyWithValue(serialized, "basicAuthCredentials", {"username": "username", "password": "password"})
        self.assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
        self.assertDictContainsKeyWithValue(serialized, "bodyAsBase64", "test3")
        self.assertDictContainsKeyWithValue(serialized, "body", "test4")

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_request_pattern_result_deserialization(self):
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
            "basicAuthCredentials": {"username": "username", "password": "password"},
            "method": "GET",
        }
        e = NearMissRequestPatternResult.from_dict(serialized)
        self.assertIsInstance(e, NearMissRequestPatternResult)
        self.assertEqual("test", e.url)
        self.assertEqual("test2", e.absolute_url)
        self.assertEqual("GET", e.method)
        self.assertEqual("1.1.1.1", e.client_ip)
        self.assertEqual({"Accept": "json"}, e.headers)
        self.assertEqual({"test": 1}, e.query_parameters)
        self.assertEqual({"chocolate": "chip"}, e.cookies)
        self.assertIsInstance(e.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.basic_auth_credentials.username)
        self.assertEqual("password", e.basic_auth_credentials.password)
        self.assertEqual(False, e.browser_proxy_request)
        self.assertEqual("test3", e.body_as_base64)
        self.assertEqual("test4", e.body)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_serialization(self):
        e = NearMissMatch(
            request=NearMissMatchRequest(url="test"),
            request_pattern=NearMissRequestPatternResult(url="test2"),
            match_result=NearMissMatchResult(distance=0.75),
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValueType(serialized, "request", dict)
        request = serialized["request"]
        self.assertDictContainsKeyWithValue(request, "url", "test")

        self.assertDictContainsKeyWithValueType(serialized, "requestPattern", dict)
        request_pattern = serialized["requestPattern"]
        self.assertDictContainsKeyWithValue(request_pattern, "url", "test2")

        self.assertDictContainsKeyWithValueType(serialized, "matchResult", dict)
        match_result = serialized["matchResult"]
        self.assertDictContainsKeyWithValue(match_result, "distance", 0.75)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_deserialization(self):
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
                "basicAuthCredentials": {"username": "username", "password": "password"},
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
                "basicAuthCredentials": {"username": "username", "password": "password"},
                "method": "GET",
            },
            "matchResult": {"distance": 0.75},
        }
        e = NearMissMatch.from_dict(serialized)
        self.assertIsInstance(e, NearMissMatch)
        self.assertIsInstance(e.request, NearMissMatchRequest)
        self.assertIsInstance(e.request_pattern, NearMissRequestPatternResult)
        self.assertIsInstance(e.match_result, NearMissMatchResult)

        # request
        self.assertEqual("test", e.request.url)
        self.assertEqual("test2", e.request.absolute_url)
        self.assertEqual("GET", e.request.method)
        self.assertEqual("1.1.1.1", e.request.client_ip)
        self.assertEqual({"Accept": "json"}, e.request.headers)
        self.assertEqual({"test": 1}, e.request.query_parameters)
        self.assertEqual({"chocolate": "chip"}, e.request.cookies)
        self.assertIsInstance(e.request.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.request.basic_auth_credentials.username)
        self.assertEqual("password", e.request.basic_auth_credentials.password)
        self.assertEqual(False, e.request.browser_proxy_request)
        self.assertEqual(12345, e.request.logged_date)
        self.assertEqual("1/1/2017 00:00:00+0000", e.request.logged_date_string)
        self.assertEqual("test3", e.request.body_as_base64)
        self.assertEqual("test4", e.request.body)

        # request pattern
        self.assertEqual("test", e.request_pattern.url)
        self.assertEqual("test2", e.request_pattern.absolute_url)
        self.assertEqual("GET", e.request_pattern.method)
        self.assertEqual("1.1.1.1", e.request_pattern.client_ip)
        self.assertEqual({"Accept": "json"}, e.request_pattern.headers)
        self.assertEqual({"test": 1}, e.request_pattern.query_parameters)
        self.assertEqual({"chocolate": "chip"}, e.request_pattern.cookies)
        self.assertIsInstance(e.request_pattern.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.request_pattern.basic_auth_credentials.username)
        self.assertEqual("password", e.request_pattern.basic_auth_credentials.password)
        self.assertEqual(False, e.request_pattern.browser_proxy_request)
        self.assertEqual("test3", e.request_pattern.body_as_base64)
        self.assertEqual("test4", e.request_pattern.body)

        # match result
        self.assertEqual(0.75, e.match_result.distance)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_response_serialization(self):
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
        self.assertDictContainsKeyWithValueType(serialized, "nearMisses", list)
        near_miss = serialized["nearMisses"][0]
        self.assertDictContainsKeyWithValueType(near_miss, "request", dict)
        self.assertDictContainsKeyWithValue(near_miss["request"], "url", "test")
        self.assertDictContainsKeyWithValueType(near_miss, "requestPattern", dict)
        self.assertDictContainsKeyWithValue(near_miss["requestPattern"], "url", "test2")
        self.assertDictContainsKeyWithValueType(near_miss, "matchResult", dict)
        self.assertDictContainsKeyWithValue(near_miss["matchResult"], "distance", 0.75)

    @attr("unit", "serialization", "nearmisses")
    def test_near_miss_match_response_deserialization(self):
        serialized = {"nearMisses": [{"request": {"url": "test"}, "requestPattern": {"url": "test"}, "matchResult": {"distance": 0.75}}]}
        e = NearMissMatchResponse.from_dict(serialized)
        self.assertIsInstance(e, NearMissMatchResponse)
        self.assertIsInstance(e.near_misses, list)
        self.assertEqual(1, len(e.near_misses))
        near_miss = e.near_misses[0]
        self.assertIsInstance(near_miss, NearMissMatch)
        self.assertIsInstance(near_miss.request, NearMissMatchRequest)
        self.assertIsInstance(near_miss.request_pattern, NearMissRequestPatternResult)
        self.assertIsInstance(near_miss.match_result, NearMissMatchResult)
