from wiremock.resources.mappings import BasicAuthCredentials
from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.resources.requests import (
    RequestResponse,
    RequestCountResponse,
    RequestResponseDefinition,
    RequestResponseAll,
    RequestResponseFindResponse,
    RequestResponseRequest,
    RequestResponseAllMeta,
)


class RequestsSerializationTests(BaseClientTestCase):
    @attr("unit", "serialization", "requests")
    def test_request_count_response_serialization(self):
        e = RequestCountResponse(count=1)
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "count", 1)

    @attr("unit", "serialization", "requests")
    def test_request_count_response_deserialization(self):
        serialized = {"count": 1}
        e = RequestCountResponse.from_dict(serialized)
        self.assertIsInstance(e, RequestCountResponse)
        self.assertEqual(1, e.count)

    @attr("unit", "serialization", "requests")
    def test_request_response_all_meta_serialization(self):
        e = RequestResponseAllMeta(total=1)
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "total", 1)

    @attr("unit", "serialization", "requests")
    def test_request_response_all_meta_deserialization(self):
        serialized = {"total": 1}
        e = RequestResponseAllMeta.from_dict(serialized)
        self.assertIsInstance(e, RequestResponseAllMeta)
        self.assertEqual(1, e.total)

    @attr("unit", "serialization", "requests")
    def test_request_response_request_serialization(self):
        e = RequestResponseRequest(
            method="GET",
            url="test",
            absolute_url="test2",
            client_ip="test3",
            basic_auth_credentials=BasicAuthCredentials(username="username", password="password"),
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
        self.assertDictContainsKeyWithValue(serialized, "method", "GET")
        self.assertDictContainsKeyWithValue(serialized, "url", "test")
        self.assertDictContainsKeyWithValue(serialized, "absoluteUrl", "test2")
        self.assertDictContainsKeyWithValue(serialized, "clientIp", "test3")
        self.assertDictContainsKeyWithValue(serialized, "basicAuthCredentials", {"username": "username", "password": "password"})
        self.assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
        self.assertDictContainsKeyWithValue(serialized, "headers", {"test": "1"})
        self.assertDictContainsKeyWithValue(serialized, "queryParameters", {"test2": "2"})
        self.assertDictContainsKeyWithValue(serialized, "browserProxyRequest", False)
        self.assertDictContainsKeyWithValue(serialized, "body", "test4")
        self.assertDictContainsKeyWithValue(serialized, "bodyAsBase64", "test5")
        self.assertDictContainsKeyWithValue(serialized, "loggedDate", 12345)
        self.assertDictContainsKeyWithValue(serialized, "loggedDateString", "test6")

    @attr("unit", "serialization", "requests")
    def test_request_response_request_deserialization(self):
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
        self.assertIsInstance(e, RequestResponseRequest)
        self.assertEqual("GET", e.method)
        self.assertEqual("test", e.url)
        self.assertEqual("test2", e.absolute_url)
        self.assertEqual("test3", e.client_ip)
        self.assertIsInstance(e.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.basic_auth_credentials.username)
        self.assertEqual("password", e.basic_auth_credentials.password)
        self.assertEqual({"chocolate": "chip"}, e.cookies)
        self.assertEqual({"test": "1"}, e.headers)
        self.assertEqual({"test2": "2"}, e.query_parameters)
        self.assertEqual(False, e.browser_proxy_request)
        self.assertEqual("test4", e.body)
        self.assertEqual("test5", e.body_as_base64)
        self.assertEqual(12345, e.logged_date)
        self.assertEqual("test6", e.logged_date_string)

    @attr("unit", "serialization", "requests")
    def test_request_response_definition_serialization(self):
        e = RequestResponseDefinition(status=200, transformers=["test"], from_configured_stub=False, transformer_parameters={"test2": "2"})
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "status", 200)
        self.assertDictContainsKeyWithValue(serialized, "transformers", ["test"])
        self.assertDictContainsKeyWithValue(serialized, "fromConfiguredStub", False)
        self.assertDictContainsKeyWithValue(serialized, "transformerParameters", {"test2": "2"})

    @attr("unit", "serialization", "requests")
    def test_request_response_definition_deserialization(self):
        serialized = {"status": 200, "transformers": ["test"], "fromConfiguredStub": False, "transformerParameters": {"test2": "2"}}
        e = RequestResponseDefinition.from_dict(serialized)
        self.assertIsInstance(e, RequestResponseDefinition)
        self.assertEqual(200, e.status)
        self.assertEqual(["test"], e.transformers)
        self.assertEqual(False, e.from_configured_stub)
        self.assertEqual({"test2": "2"}, e.transformer_parameters)

    @attr("unit", "serialization", "requests")
    def test_request_response_serialization(self):
        e = RequestResponse(request=RequestResponseRequest(method="GET", url="test"), response_definition=RequestResponseDefinition(status=200))
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "request", {"method": "GET", "url": "test"})
        self.assertDictContainsKeyWithValue(serialized, "responseDefinition", {"status": 200})

    @attr("unit", "serialization", "requests")
    def test_request_response_deserialization(self):
        serialized = {"request": {"method": "GET", "url": "test"}, "responseDefinition": {"status": 200}}
        e = RequestResponse.from_dict(serialized)
        self.assertIsInstance(e, RequestResponse)
        self.assertIsInstance(e.request, RequestResponseRequest)
        self.assertEqual("GET", e.request.method)
        self.assertEqual("test", e.request.url)
        self.assertIsInstance(e.response_definition, RequestResponseDefinition)
        self.assertEqual(200, e.response_definition.status)

    @attr("unit", "serialization", "requests")
    def test_request_response_find_response_serialization(self):
        e = RequestResponseFindResponse(requests=[RequestResponseRequest(method="GET", url="test"),])
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValueType(serialized, "requests", list)
        self.assertDictContainsKeyWithValue(serialized, "requests", [{"method": "GET", "url": "test"},])

    @attr("unit", "serialization", "requests")
    def test_request_response_find_response_deserialization(self):
        serialized = {"requests": [{"method": "GET", "url": "test"},]}
        e = RequestResponseFindResponse.from_dict(serialized)
        self.assertIsInstance(e, RequestResponseFindResponse)
        self.assertIsInstance(e.requests, list)
        self.assertIsInstance(e.requests[0], RequestResponseRequest)
        self.assertEqual("GET", e.requests[0].method)
        self.assertEqual("test", e.requests[0].url)

    @attr("unit", "serialization", "requests")
    def test_request_response_all_serialization(self):
        e = RequestResponseAll(
            requests=[
                RequestResponse(request=RequestResponseRequest(method="GET", url="test"), response_definition=RequestResponseDefinition(status=200)),
            ],
            meta=RequestResponseAllMeta(total=1),
            request_journal_disabled=False,
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "requestJournalDisabled", False)
        self.assertDictContainsKeyWithValue(
            serialized, "requests", [{"request": {"method": "GET", "url": "test"}, "responseDefinition": {"status": 200}},]
        )
        self.assertDictContainsKeyWithValue(serialized, "meta", {"total": 1})

    @attr("unit", "serialization", "requests")
    def test_request_response_all_deserialization(self):
        serialized = {
            "requests": [{"request": {"method": "GET", "url": "test"}, "responseDefinition": {"status": 200}},],
            "meta": {"total": 1},
            "requestJournalDisabled": False,
        }
        e = RequestResponseAll.from_dict(serialized)
        self.assertIsInstance(e, RequestResponseAll)
        self.assertEqual(False, e.request_journal_disabled)
        self.assertIsInstance(e.requests, list)
        rr = e.requests[0]
        self.assertIsInstance(rr, RequestResponse)
        self.assertIsInstance(rr.request, RequestResponseRequest)
        self.assertEqual("GET", rr.request.method)
        self.assertEqual("test", rr.request.url)
        self.assertIsInstance(rr.response_definition, RequestResponseDefinition)
        self.assertEqual(200, rr.response_definition.status)
        self.assertIsInstance(e.meta, RequestResponseAllMeta)
        self.assertEqual(1, e.meta.total)
