from tests.utils import (
    assertDictContainsKeyWithValue,
    assertDictContainsKeyWithValueType,
    assertEqual,
    assertIsInstance,
)
from wiremock.resources.mappings import BasicAuthCredentials
from wiremock.resources.requests import (
    RequestCountResponse,
    RequestResponse,
    RequestResponseAll,
    RequestResponseAllMeta,
    RequestResponseDefinition,
    RequestResponseFindResponse,
    RequestResponseRequest,
)


def test_request_count_response_serialization():
    e = RequestCountResponse(count=1)
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "count", 1)


def test_request_count_response_deserialization():
    serialized = {"count": 1}
    e = RequestCountResponse.from_dict(serialized)
    assertIsInstance(e, RequestCountResponse)
    assertEqual(1, e.count)


def test_request_response_all_meta_serialization():
    e = RequestResponseAllMeta(total=1)
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "total", 1)


def test_request_response_all_meta_deserialization():
    serialized = {"total": 1}
    e = RequestResponseAllMeta.from_dict(serialized)
    assertIsInstance(e, RequestResponseAllMeta)
    assertEqual(1, e.total)


def test_request_response_request_serialization():
    e = RequestResponseRequest(
        method="GET",
        url="test",
        absolute_url="test2",
        client_ip="test3",
        basic_auth_credentials=BasicAuthCredentials(
            username="username", password="password"
        ),
        cookies={"chocolate": "chip"},
        headers={"test": "1"},
        query_parameters={"test2": "2"},
        browser_proxy_request=False,
        body="test4",
        body_as_base64="test5",
        logged_date=12345,
        logged_date_string="test6",
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "method", "GET")
    assertDictContainsKeyWithValue(serialized, "url", "test")
    assertDictContainsKeyWithValue(serialized, "absoluteUrl", "test2")
    assertDictContainsKeyWithValue(serialized, "clientIp", "test3")
    assertDictContainsKeyWithValue(
        serialized,
        "basicAuthCredentials",
        {"username": "username", "password": "password"},
    )
    assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
    assertDictContainsKeyWithValue(serialized, "headers", {"test": "1"})
    assertDictContainsKeyWithValue(serialized, "queryParameters", {"test2": "2"})
    assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
    assertDictContainsKeyWithValue(serialized, "body", "test4")
    assertDictContainsKeyWithValue(serialized, "bodyAsBase64", "test5")
    assertDictContainsKeyWithValue(serialized, "loggedDate", 12345)
    assertDictContainsKeyWithValue(serialized, "loggedDateString", "test6")


def test_request_response_request_deserialization():
    serialized = {
        "method": "GET",
        "url": "test",
        "absoluteUrl": "test2",
        "clientIp": "test3",
        "basicAuthCredentials": {"username": "username", "password": "password"},
        "cookies": {"chocolate": "chip"},
        "headers": {"test": "1"},
        "queryParameters": {"test2": "2"},
        "browserProxyRequest": False,
        "body": "test4",
        "bodyAsBase64": "test5",
        "loggedDate": 12345,
        "loggedDateString": "test6",
    }
    e = RequestResponseRequest.from_dict(serialized)
    assertIsInstance(e, RequestResponseRequest)
    assertEqual("GET", e.method)
    assertEqual("test", e.url)
    assertEqual("test2", e.absolute_url)
    assertEqual("test3", e.client_ip)
    assertIsInstance(e.basic_auth_credentials, BasicAuthCredentials)
    assertEqual("username", e.basic_auth_credentials.username)
    assertEqual("password", e.basic_auth_credentials.password)
    assertEqual({"chocolate": "chip"}, e.cookies)
    assertEqual({"test": "1"}, e.headers)
    assertEqual({"test2": "2"}, e.query_parameters)
    assertEqual(False, e.browser_proxy_request)
    assertEqual("test4", e.body)
    assertEqual("test5", e.body_as_base64)
    assertEqual(12345, e.logged_date)
    assertEqual("test6", e.logged_date_string)


def test_request_response_definition_serialization():
    e = RequestResponseDefinition(
        status=200,
        transformers=["test"],
        from_configured_stub=False,
        transformer_parameters={"test2": "2"},
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "status", 200)
    assertDictContainsKeyWithValue(serialized, "transformers", ["test"])
    assertDictContainsKeyWithValue(serialized, "fromConfiguredStub", False)
    assertDictContainsKeyWithValue(serialized, "transformerParameters", {"test2": "2"})


def test_request_response_definition_deserialization():
    serialized = {
        "status": 200,
        "transformers": ["test"],
        "fromConfiguredStub": False,
        "transformerParameters": {"test2": "2"},
    }
    e = RequestResponseDefinition.from_dict(serialized)
    assertIsInstance(e, RequestResponseDefinition)
    assertEqual(200, e.status)
    assertEqual(["test"], e.transformers)
    assertEqual(False, e.from_configured_stub)
    assertEqual({"test2": "2"}, e.transformer_parameters)


def test_request_response_serialization():
    e = RequestResponse(
        request=RequestResponseRequest(method="GET", url="test"),
        response_definition=RequestResponseDefinition(status=200),
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(
        serialized, "request", {"method": "GET", "url": "test"}
    )
    assertDictContainsKeyWithValue(serialized, "responseDefinition", {"status": 200})


def test_request_response_deserialization():
    serialized = {
        "request": {"method": "GET", "url": "test"},
        "responseDefinition": {"status": 200},
    }
    e = RequestResponse.from_dict(serialized)
    assertIsInstance(e, RequestResponse)
    assertIsInstance(e.request, RequestResponseRequest)
    assertEqual("GET", e.request.method)
    assertEqual("test", e.request.url)
    assertIsInstance(e.response_definition, RequestResponseDefinition)
    assertEqual(200, e.response_definition.status)


def test_request_response_find_response_serialization():
    e = RequestResponseFindResponse(
        requests=[
            RequestResponseRequest(method="GET", url="test"),
        ]
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValueType(serialized, "requests", list)
    assertDictContainsKeyWithValue(
        serialized,
        "requests",
        [
            {"method": "GET", "url": "test"},
        ],
    )


def test_request_response_find_response_deserialization():
    serialized = {
        "requests": [
            {"method": "GET", "url": "test"},
        ]
    }
    e = RequestResponseFindResponse.from_dict(serialized)
    assertIsInstance(e, RequestResponseFindResponse)
    assertIsInstance(e.requests, list)
    assertIsInstance(e.requests[0], RequestResponseRequest)
    assertEqual("GET", e.requests[0].method)
    assertEqual("test", e.requests[0].url)


def test_request_response_all_serialization():
    e = RequestResponseAll(
        requests=[
            RequestResponse(
                request=RequestResponseRequest(method="GET", url="test"),
                response_definition=RequestResponseDefinition(status=200),
            ),
        ],
        meta=RequestResponseAllMeta(total=1),
        request_journal_disabled=False,
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(serialized, "requestJournalDisabled", False)
    assertDictContainsKeyWithValue(
        serialized,
        "requests",
        [
            {
                "request": {"method": "GET", "url": "test"},
                "responseDefinition": {"status": 200},
            },
        ],
    )
    assertDictContainsKeyWithValue(serialized, "meta", {"total": 1})


def test_request_response_all_deserialization():
    serialized = {
        "requests": [
            {
                "request": {"method": "GET", "url": "test"},
                "responseDefinition": {"status": 200},
            },
        ],
        "meta": {"total": 1},
        "requestJournalDisabled": False,
    }
    e = RequestResponseAll.from_dict(serialized)
    assertIsInstance(e, RequestResponseAll)
    assertEqual(False, e.request_journal_disabled)
    assertIsInstance(e.requests, list)
    rr = e.requests[0]
    assertIsInstance(rr, RequestResponse)
    assertIsInstance(rr.request, RequestResponseRequest)
    assertEqual("GET", rr.request.method)
    assertEqual("test", rr.request.url)
    assertIsInstance(rr.response_definition, RequestResponseDefinition)
    assertEqual(200, rr.response_definition.status)
    assertIsInstance(e.meta, RequestResponseAllMeta)
    assertEqual(1, e.meta.total)
