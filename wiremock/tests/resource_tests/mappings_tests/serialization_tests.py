from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.resources.mappings import (
    BasicAuthCredentials,
    Mapping,
    MappingRequest,
    MappingMeta,
    MappingResponse,
    AllMappings,
    DelayDistribution,
    DelayDistributionMethods,
)


class MappingsSerializationTests(BaseClientTestCase):
    @attr("unit", "serialization", "mappings")
    def test_basic_auth_credentials_serialization(self):
        e = BasicAuthCredentials(username="username", password="password")
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "username", "username")
        self.assertDictContainsKeyWithValue(serialized, "password", "password")

    @attr("unit", "serialization", "mappings")
    def test_basic_auth_credentials_deserialization(self):
        serialized = {"username": "username", "password": "password"}
        e = BasicAuthCredentials.from_dict(serialized)
        self.assertIsInstance(e, BasicAuthCredentials)
        self.assertEqual("username", e.username)
        self.assertEqual("password", e.password)

    @attr("unit", "serialization", "mappings")
    def test_mapping_meta_serialization(self):
        e = MappingMeta(total=1)
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "total", 1)

    @attr("unit", "serialization", "mappings")
    def test_mapping_meta_deserialization(self):
        serialized = {"total": 1}
        e = MappingMeta.from_dict(serialized)
        self.assertIsInstance(e, MappingMeta)
        self.assertEqual(1, e.total)

    @attr("unit", "serialization", "mappings")
    def test_delay_distribution_serialization(self):
        e = DelayDistribution(distribution_type=DelayDistributionMethods.LOG_NORMAL, median=0.1, sigma=0.2, upper=4, lower=3)
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "type", "lognormal")
        self.assertDictContainsKeyWithValue(serialized, "median", 0.1)
        self.assertDictContainsKeyWithValue(serialized, "sigma", 0.2)
        self.assertDictContainsKeyWithValue(serialized, "lower", 3)
        self.assertDictContainsKeyWithValue(serialized, "upper", 4)

    @attr("unit", "serialization", "mappings")
    def test_delay_distribution_deserialization(self):
        serialized = {"type": "lognormal", "median": 0.1, "sigma": 0.2, "lower": 3, "upper": 4}
        e = DelayDistribution.from_dict(serialized)
        self.assertIsInstance(e, DelayDistribution)
        self.assertEqual("lognormal", e.distribution_type)
        self.assertEqual(0.1, e.median)
        self.assertEqual(0.2, e.sigma)
        self.assertEqual(3, e.lower)
        self.assertEqual(4, e.upper)

    @attr("unit", "serialization", "mappings")
    def test_mapping_request_serialization(self):
        e = MappingRequest(
            method="GET",
            url="test1",
            url_path="test2",
            url_path_pattern="test3",
            url_pattern="test4",
            basic_auth_credentials=BasicAuthCredentials(username="username", password="password"),
            cookies={"chocolate": "chip"},
            headers={"Accept": "stuff"},
            query_parameters={"param": "1"},
            body_patterns={"test": "test2"},
            metadata={'key': 'value'}
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "method", "GET")
        self.assertDictContainsKeyWithValue(serialized, "url", "test1")
        self.assertDictContainsKeyWithValue(serialized, "urlPath", "test2")
        self.assertDictContainsKeyWithValue(serialized, "urlPathPattern", "test3")
        self.assertDictContainsKeyWithValue(serialized, "urlPattern", "test4")
        self.assertDictContainsKeyWithValue(serialized, "basicAuthCredentials", {"username": "username", "password": "password"})
        self.assertDictContainsKeyWithValue(serialized, "cookies", {"chocolate": "chip"})
        self.assertDictContainsKeyWithValue(serialized, "headers", {"Accept": "stuff"})
        self.assertDictContainsKeyWithValue(serialized, "queryParameters", {"param": "1"})
        self.assertDictContainsKeyWithValue(serialized, "bodyPatterns", {"test": "test2"})
        self.assertDictContainsKeyWithValue(serialized, "metadata", {"key": "value"})

    @attr("unit", "serialization", "mappings")
    def test_mapping_request_deserialization(self):
        serialized = {
            "method": "GET",
            "url": "test1",
            "urlPath": "test2",
            "urlPathPattern": "test3",
            "urlPattern": "test4",
            "basicAuthCredentials": {"username": "username", "password": "password"},
            "cookies": {"chocolate": "chip"},
            "headers": {"Accept": "stuff"},
            "queryParameters": {"param": "1"},
            "bodyPatterns": {"test": "test2"},
            'metadata': {'key': [1, 2, 3]},
        }
        e = MappingRequest.from_dict(serialized)
        self.assertIsInstance(e, MappingRequest)
        self.assertEqual("GET", e.method)
        self.assertEqual("test1", e.url)
        self.assertEqual("test2", e.url_path)
        self.assertEqual("test3", e.url_path_pattern)
        self.assertEqual("test4", e.url_pattern)
        self.assertIsInstance(e.basic_auth_credentials, BasicAuthCredentials)
        self.assertEqual("username", e.basic_auth_credentials.username)
        self.assertEqual("password", e.basic_auth_credentials.password)
        self.assertEqual({"chocolate": "chip"}, e.cookies)
        self.assertEqual({"Accept": "stuff"}, e.headers)
        self.assertEqual({"param": "1"}, e.query_parameters)
        self.assertEqual({"test": "test2"}, e.body_patterns)
        self.assertEqual({"key": [1, 2, 3]}, e.metadata)

    @attr("unit", "serialization", "mappings")
    def test_mapping_response_serialization(self):
        e = MappingResponse(
            additional_proxy_request_headers={"test": "1"},
            base64_body="test2",
            body="test3",
            body_file_name="test4",
            json_body="test5",
            delay_distribution=DelayDistribution(distribution_type="lognormal", sigma=0.1, median=0.2),
            fault="test6",
            fixed_delay_milliseconds=500,
            from_configured_stub="test7",
            headers={"test": "1"},
            proxy_base_url="test8",
            status=200,
            status_message="test9",
            transformer_parameters={"test2": "2"},
            transformers=["test10"],
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "additionalProxyRequestHeaders", {"test": "1"})
        self.assertDictContainsKeyWithValue(serialized, "base64Body", "test2")
        self.assertDictContainsKeyWithValue(serialized, "body", "test3")
        self.assertDictContainsKeyWithValue(serialized, "bodyFileName", "test4")
        self.assertDictContainsKeyWithValue(serialized, "jsonBody", "test5")
        self.assertDictContainsKeyWithValue(serialized, "delayDistribution", {"type": "lognormal", "sigma": 0.1, "median": 0.2})
        self.assertDictContainsKeyWithValue(serialized, "fault", "test6")
        self.assertDictContainsKeyWithValue(serialized, "fixedDelayMilliseconds", 500)
        self.assertDictContainsKeyWithValue(serialized, "fromConfiguredStub", "test7")
        self.assertDictContainsKeyWithValue(serialized, "headers", {"test": "1"})
        self.assertDictContainsKeyWithValue(serialized, "proxyBaseUrl", "test8")
        self.assertDictContainsKeyWithValue(serialized, "status", 200)
        self.assertDictContainsKeyWithValue(serialized, "statusMessage", "test9")
        self.assertDictContainsKeyWithValue(serialized, "transformerParameters", {"test2": "2"})
        self.assertDictContainsKeyWithValue(serialized, "transformers", ["test10"])

    @attr("unit", "serialization", "mappings")
    def test_mapping_response_deserialization(self):
        serialized = {
            "additionalProxyRequestHeaders": {"test": "1"},
            "base64Body": "test2",
            "body": "test3",
            "bodyFileName": "test4",
            "jsonBody": "test5",
            "delayDistribution": {"type": "lognormal", "sigma": 0.1, "median": 0.2},
            "fault": "test6",
            "fixedDelayMilliseconds": 500,
            "fromConfiguredStub": "test7",
            "headers": {"test": "1"},
            "proxyBaseUrl": "test8",
            "status": 200,
            "statusMessage": "test9",
            "transformerParameters": {"test2": "2"},
            "transformers": ["test10"],
        }
        e = MappingResponse.from_dict(serialized)
        self.assertIsInstance(e, MappingResponse)
        self.assertEqual({"test": "1"}, e.additional_proxy_request_headers)
        self.assertEqual("test2", e.base64_body)
        self.assertEqual("test3", e.body)
        self.assertEqual("test4", e.body_file_name)
        self.assertEqual("test5", e.json_body)
        self.assertIsInstance(e.delay_distribution, DelayDistribution)
        self.assertEqual("lognormal", e.delay_distribution.distribution_type)
        self.assertEqual("test6", e.fault)
        self.assertEqual(500, e.fixed_delay_milliseconds)
        self.assertEqual("test7", e.from_configured_stub)
        self.assertEqual({"test": "1"}, e.headers)
        self.assertEqual("test8", e.proxy_base_url)
        self.assertEqual(200, e.status)
        self.assertEqual("test9", e.status_message)
        self.assertEqual({"test2": "2"}, e.transformer_parameters)
        self.assertEqual(["test10"], e.transformers)

    @attr("unit", "serialization", "mappings")
    def test_mapping_serialization(self):
        e = Mapping(
            priority=1,
            request=MappingRequest(method="GET", url="test"),
            response=MappingResponse(status=200, status_message="test2"),
            persistent=False,
            post_serve_actions={"test": "1"},
            new_scenario_state="test3",
            required_scenario_state="test4",
            scenario_name="test5",
        )
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "priority", 1)
        self.assertDictContainsKeyWithValue(serialized, "request", {"method": "GET", "url": "test"})
        self.assertDictContainsKeyWithValue(serialized, "response", {"status": 200, "statusMessage": "test2"})
        self.assertDictContainsKeyWithValue(serialized, "persistent", False)
        self.assertDictContainsKeyWithValue(serialized, "postServeActions", {"test": "1"})
        self.assertDictContainsKeyWithValue(serialized, "newScenarioState", "test3")
        self.assertDictContainsKeyWithValue(serialized, "requiredScenarioState", "test4")
        self.assertDictContainsKeyWithValue(serialized, "scenarioName", "test5")

    @attr("unit", "serialization", "mappings")
    def test_mapping_deserialization(self):
        serialized = {
            "priority": 1,
            "request": {"method": "GET", "url": "test"},
            "response": {"status": 200, "statusMessage": "test2"},
            "persistent": False,
            "postServeActions": {"test": "1"},
            "newScenarioState": "test3",
            "requiredScenarioState": "test4",
            "scenarioName": "test5",
        }
        e = Mapping.from_dict(serialized)
        self.assertIsInstance(e, Mapping)
        self.assertEqual(1, e.priority)
        self.assertIsInstance(e.request, MappingRequest)
        self.assertEqual("GET", e.request.method)
        self.assertEqual("test", e.request.url)
        self.assertIsInstance(e.response, MappingResponse)
        self.assertEqual(200, e.response.status)
        self.assertEqual("test2", e.response.status_message)
        self.assertEqual(False, e.persistent)
        self.assertEqual({"test": "1"}, e.post_serve_actions)
        self.assertEqual("test3", e.new_scenario_state)
        self.assertEqual("test4", e.required_scenario_state)
        self.assertEqual("test5", e.scenario_name)

    @attr("unit", "serialization", "mappings")
    def test_all_mappings_serialization(self):
        e = AllMappings(mappings=[Mapping(priority=1), ], meta=MappingMeta(total=1))
        serialized = e.get_json_data()
        self.assertDictContainsKeyWithValue(serialized, "mappings", [{"priority": 1}, ])
        self.assertDictContainsKeyWithValue(serialized, "meta", {"total": 1})

    @attr("unit", "serialization", "mappings")
    def test_all_mappings_deserialization(self):
        serialized = {"mappings": [{"priority": 1}, ], "meta": {"total": 1}}
        e = AllMappings.from_dict(serialized)
        self.assertIsInstance(e, AllMappings)
        self.assertIsInstance(e.mappings, list)
        m = e.mappings[0]
        self.assertIsInstance(m, Mapping)
        self.assertEqual(1, m.priority)
        self.assertIsInstance(e.meta, MappingMeta)
        self.assertEqual(1, e.meta.total)
