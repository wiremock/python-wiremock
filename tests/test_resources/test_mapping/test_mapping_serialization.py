import pytest

from tests.utils import assertDictContainsKeyWithValue
from wiremock.resources.mappings import (
    AllMappings,
    BasicAuthCredentials,
    DelayDistribution,
    DelayDistributionMethods,
    Mapping,
    MappingMeta,
    MappingRequest,
    MappingResponse,
)


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_basic_auth_credentials_serialization():
    e = BasicAuthCredentials(username="username", password="password")
    serialized = e.get_json_data()
    assert serialized["username"] == "username"
    assert serialized["password"] == "password"


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_basic_auth_credentials_deserialization():
    serialized = {"username": "username", "password": "password"}
    e = BasicAuthCredentials.from_dict(serialized)
    assert isinstance(e, BasicAuthCredentials)
    assert e.username == "username"
    assert e.password == "password"


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_meta_serialization():
    e = MappingMeta(total=1)
    serialized = e.get_json_data()
    assert serialized["total"] == 1


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_meta_deserialization():
    serialized = {"total": 1}
    e = MappingMeta.from_dict(serialized)
    assert isinstance(e, MappingMeta)
    assert e.total == 1


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_delay_distribution_serialization():
    e = DelayDistribution(
        distribution_type=DelayDistributionMethods.LOG_NORMAL,
        median=0.1,
        sigma=0.2,
        upper=4,
        lower=3,
    )
    serialized = e.get_json_data()
    assert serialized["type"] == "lognormal"
    assert serialized["median"] == 0.1
    assert serialized["sigma"] == 0.2
    assert serialized["lower"] == 3
    assert serialized["upper"] == 4


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_delay_distribution_deserialization():
    serialized = {
        "type": "lognormal",
        "median": 0.1,
        "sigma": 0.2,
        "lower": 3,
        "upper": 4,
    }
    e = DelayDistribution.from_dict(serialized)
    assert isinstance(e, DelayDistribution)
    assert e.distribution_type == "lognormal"
    assert e.median == 0.1
    assert e.sigma == 0.2
    assert e.lower == 3
    assert e.upper == 4


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_request_serialization():
    e = MappingRequest(
        method="GET",
        url="test1",
        url_path="test2",
        url_path_pattern="test3",
        url_pattern="test4",
        basic_auth_credentials=BasicAuthCredentials(
            username="username", password="password"
        ),
        cookies={"chocolate": "chip"},
        headers={"Accept": "stuff"},
        query_parameters={"param": "1"},
        body_patterns={"test": "test2"},
        metadata={"key": "value"},
    )
    serialized = e.get_json_data()
    assert serialized["method"] == "GET"
    assert serialized["url"] == "test1"
    assert serialized["urlPath"] == "test2"
    assert serialized["urlPathPattern"] == "test3"
    assert serialized["urlPattern"] == "test4"
    assert serialized["basicAuthCredentials"] == {
        "username": "username",
        "password": "password",
    }
    assert serialized["cookies"] == {"chocolate": "chip"}
    assert serialized["headers"] == {"Accept": "stuff"}

    assert serialized["queryParameters"] == {"param": "1"}
    assert serialized["bodyPatterns"] == {"test": "test2"}
    assert serialized["metadata"] == {"key": "value"}


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_request_deserialization():
    serialized = {
        "method": "GET",
        "url": "test1",
        "urlPath": "test2",
        "urlPathPattern": "test3",
        "urlPattern": "test4",
        "basicAuthCredentials": {
            "username": "username",
            "password": "password",
        },
        "cookies": {"chocolate": "chip"},
        "headers": {"Accept": "stuff"},
        "queryParameters": {"param": "1"},
        "bodyPatterns": {"test": "test2"},
        "metadata": {"key": [1, 2, 3]},
    }
    e = MappingRequest.from_dict(serialized)
    assert isinstance(e, MappingRequest)
    assert "GET" == e.method
    assert "test1" == e.url
    assert "test2" == e.url_path
    assert "test3" == e.url_path_pattern
    assert "test4" == e.url_pattern
    assert isinstance(e.basic_auth_credentials, BasicAuthCredentials)
    assert "username" == e.basic_auth_credentials.username
    assert "password" == e.basic_auth_credentials.password
    assert {"chocolate": "chip"} == e.cookies
    assert {"Accept": "stuff"} == e.headers
    assert {"param": "1"} == e.query_parameters
    assert {"test": "test2"} == e.body_patterns
    assert {"key": [1, 2, 3]} == e.metadata


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_response_serialization():
    e = MappingResponse(
        additional_proxy_request_headers={"test": "1"},
        base64_body="test2",
        body="test3",
        body_file_name="test4",
        json_body="test5",
        delay_distribution=DelayDistribution(
            distribution_type="lognormal", sigma=0.1, median=0.2
        ),
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
    assertDictContainsKeyWithValue(
        serialized, "additionalProxyRequestHeaders", {"test": "1"}
    )
    assertDictContainsKeyWithValue(serialized, "base64Body", "test2")
    assertDictContainsKeyWithValue(serialized, "body", "test3")
    assertDictContainsKeyWithValue(serialized, "bodyFileName", "test4")
    assertDictContainsKeyWithValue(serialized, "jsonBody", "test5")
    assertDictContainsKeyWithValue(
        serialized,
        "delayDistribution",
        {
            "type": "lognormal",
            "sigma": 0.1,
            "median": 0.2,
        },
    )
    assertDictContainsKeyWithValue(serialized, "fault", "test6")
    assertDictContainsKeyWithValue(serialized, "fixedDelayMilliseconds", 500)
    assertDictContainsKeyWithValue(serialized, "fromConfiguredStub", "test7")
    assertDictContainsKeyWithValue(serialized, "headers", {"test": "1"})
    assertDictContainsKeyWithValue(serialized, "proxyBaseUrl", "test8")
    assertDictContainsKeyWithValue(serialized, "status", 200)
    assertDictContainsKeyWithValue(serialized, "statusMessage", "test9")
    assertDictContainsKeyWithValue(
        serialized,
        "transformerParameters",
        {"test2": "2"},
    )
    assertDictContainsKeyWithValue(serialized, "transformers", ["test10"])


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_response_deserialization():
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
    assert isinstance(e, MappingResponse)
    assert e.additional_proxy_request_headers == {"test": "1"}
    assert e.base64_body == "test2"
    assert e.body == "test3"
    assert e.body_file_name == "test4"
    assert e.json_body == "test5"
    assert isinstance(e.delay_distribution, DelayDistribution)
    assert e.delay_distribution.distribution_type == "lognormal"
    assert e.fault == "test6"
    assert e.fixed_delay_milliseconds == 500
    assert e.from_configured_stub == "test7"
    assert e.headers == {"test": "1"}
    assert e.proxy_base_url == "test8"
    assert e.status == 200
    assert e.status_message == "test9"
    assert e.transformer_parameters == {"test2": "2"}
    assert e.body == "test3"
    assert e.body_file_name == "test4"
    assert e.json_body == "test5"
    assert isinstance(e.delay_distribution, DelayDistribution)
    assert e.delay_distribution.distribution_type == "lognormal"
    assert e.fault == "test6"
    assert e.fixed_delay_milliseconds == 500
    assert e.from_configured_stub == "test7"
    assert e.headers == {"test": "1"}
    assert e.proxy_base_url == "test8"
    assert e.status == 200
    assert e.status_message == "test9"
    assert e.transformer_parameters == {"test2": "2"}
    assert e.transformers == ["test10"]


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_serialization():
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

    assertDictContainsKeyWithValue(serialized, "priority", 1)
    assertDictContainsKeyWithValue(
        serialized,
        "request",
        {
            "method": "GET",
            "url": "test",
        },
    )
    assertDictContainsKeyWithValue(
        serialized,
        "response",
        {
            "status": 200,
            "statusMessage": "test2",
        },
    )
    assertDictContainsKeyWithValue(serialized, "persistent", False)

    assertDictContainsKeyWithValue(
        serialized,
        "postServeActions",
        {"test": "1"},
    )
    assertDictContainsKeyWithValue(serialized, "newScenarioState", "test3")
    assertDictContainsKeyWithValue(
        serialized,
        "requiredScenarioState",
        "test4",
    )
    assertDictContainsKeyWithValue(serialized, "scenarioName", "test5")


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_mapping_deserialization():
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
    assert isinstance(e, Mapping)
    assert e.priority == 1
    assert isinstance(e.request, MappingRequest)
    assert e.request.method == "GET"
    assert e.request.url == "test"
    assert isinstance(e.response, MappingResponse)
    assert e.response.status == 200
    assert e.response.status_message == "test2"
    assert e.persistent is False
    assert e.post_serve_actions == {"test": "1"}
    assert e.new_scenario_state == "test3"
    assert e.required_scenario_state == "test4"
    assert e.scenario_name == "test5"


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_all_mappings_serialization():
    e = AllMappings(
        mappings=[
            Mapping(priority=1),
        ],
        meta=MappingMeta(total=1),
    )
    serialized = e.get_json_data()
    assertDictContainsKeyWithValue(
        serialized,
        "mappings",
        [
            {"priority": 1},
        ],
    )
    assertDictContainsKeyWithValue(serialized, "meta", {"total": 1})


@pytest.mark.unit
@pytest.mark.serialization
@pytest.mark.mappings
def test_all_mappings_deserialization():
    serialized = {
        "mappings": [
            {"priority": 1},
        ],
        "meta": {"total": 1},
    }
    e = AllMappings.from_dict(serialized)
    assert isinstance(e, AllMappings)
    assert isinstance(e.mappings, list)
    m = e.mappings[0]
    assert isinstance(m, Mapping)
    assert m.priority == 1
    assert isinstance(e.meta, MappingMeta)
    assert e.meta.total == 1
