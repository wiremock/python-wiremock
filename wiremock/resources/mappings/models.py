from wiremock._compat import add_metaclass
from wiremock.base import BaseEntity, JsonProperty, BaseAbstractEntity, BaseEntityMetaType


class HttpMethods(object):
    ANY = "ANY"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class CommonHeaders(object):
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCEPT = "Accept"
    ACCEPT_CHARSET = "Accept-Charset"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_DATETIME = "Accept-Datetime"
    ACCEPT_PATCH = "Accept-Patch"
    ACCEPT_RANGES = "Accept-Ranges"
    AGE = "Age"
    ALLOW = "Allow"
    AUTHORIZATION = "Authorization"
    CACHE_CONTROL = "Cache-Control"
    CONNECTION = "Connection"
    COOKIE = "Cookie"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_MD5 = "Content-MD5"
    CONTENT_TYPE = "Content-Type"
    DATE = "Date"
    DNT = "DNT"
    ETAG = "ETag"
    EXPECT = "Expect"
    EXPIRES = "Expires"
    FORWARDED = "Forwarded"
    FROM = "From"
    HOST = "Host"
    IF_MATCH = "If-Match"
    IF_MODIFIED_SINCE = "If-Modified-Since"
    IF_NONE_MATCH = "If-None-Match"
    IF_RANGE = "If-Range"
    IF_UNMODIFIED_SINCE = "If-Unmodified-Since"
    LAST_MODIFIED = "Last-Modified"
    LINK = "Link"
    LOCATION = "Location"
    MAX_FORWARDS = "Max-Forwards"
    ORIGIN = "Origin"
    PRAGMA = "Pragma"
    PROXY_AUTHORIZATION = "Proxy-Authorization"
    PROXY_CONNECTION = "Proxy-Connection"
    RANGE = "Range"
    REFERER = "Referer"
    SERVER = "Server"
    SET_COOKIE = "Set-Cookie"
    TE = "TE"
    USER_AGENT = "user-agent"
    UPGRADE = "Upgrade"
    VIA = "Via"
    WARNING = "Warning"
    X_CSRF_TOKEN = "X-Csrf-TOken"
    X_FORWARDED_FOR = "X-Forwarded-For"
    X_FORWARDED_HOST = "X-Forwarded-Host"
    X_FORWARDED_PROTO = "X-Forwarded-Proto"
    X_REQUEST_ID = "X-Request-ID"
    X_CORRELATION_ID = "X-Correlation-ID"
    X_REQUESTED_WITH = "X-Requested-With"


class WireMockMatchers(object):
    ABSENT = "absent"
    ANYTHING = "anything"
    CASE_INSENSITIVE = "caseInsensitive"  # Should be true/false
    CONTAINS = "contains"
    DOES_NOT_MATCH = "doesNotMatch"
    EQUAL_TO = "equalTo"
    EQUAL_TO_JSON = "equalToJson"
    EQUAL_TO_XML = "equalToXml"
    IGNORE_ARRAY_ORDER = "ignoreArrayOrder"  # Should be true/false
    IGNORE_EXTRA_ELEMENTS = "ignoreExtraElements"  # Should be true/false
    MATCHES = "matches"
    MATCHES_JSON_PATH = "matchesJsonPath"
    MATCHES_X_PATH = "matchesXPath"
    X_PATH_NAMESPACES = "xPathNamespaces"


@add_metaclass(BaseEntityMetaType)
class BasicAuthCredentials(BaseAbstractEntity):
    username = JsonProperty("username")
    password = JsonProperty("password")


class DelayDistributionMethods(object):
    LOG_NORMAL = "lognormal"
    UNIFORM = "uniform"


class ResponseFaultType(object):
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    MALFORMED_RESPONSE_CHUNK = "MALFORMED_RESPONSE_CHUNK"
    RANDOM_DATA_THEN_CLOSE = "RANDOM_DATA_THEN_CLOSE"


@add_metaclass(BaseEntityMetaType)
class DelayDistribution(BaseAbstractEntity):
    distribution_type = JsonProperty("type")

    # lognormal
    median = JsonProperty("median")
    sigma = JsonProperty("sigma")

    # uniform
    upper = JsonProperty("upper")
    lower = JsonProperty("lower")


@add_metaclass(BaseEntityMetaType)
class MappingRequest(BaseAbstractEntity):
    method = JsonProperty("method")
    url = JsonProperty("url")
    url_path = JsonProperty("urlPath")
    url_path_pattern = JsonProperty("urlPathPattern")
    url_pattern = JsonProperty("urlPattern")
    basic_auth_credentials = JsonProperty("basicAuthCredentials", klass=BasicAuthCredentials)
    cookies = JsonProperty("cookies", klass=dict)
    headers = JsonProperty("headers", klass=dict)
    query_parameters = JsonProperty("queryParameters", klass=dict)
    body_patterns = JsonProperty("bodyPatterns", klass=list, list_klass=dict)


@add_metaclass(BaseEntityMetaType)
class MappingResponse(BaseAbstractEntity):
    additional_proxy_request_headers = JsonProperty("additionalProxyRequestHeaders", klass=dict)
    base64_body = JsonProperty("base64Body")
    body = JsonProperty("body")
    body_file_name = JsonProperty("bodyFileName")
    json_body = JsonProperty("jsonBody")
    delay_distribution = JsonProperty("delayDistribution", klass=DelayDistribution)
    fault = JsonProperty("fault")
    fixed_delay_milliseconds = JsonProperty("fixedDelayMilliseconds")
    from_configured_stub = JsonProperty("fromConfiguredStub")
    headers = JsonProperty("headers", klass=dict)
    proxy_base_url = JsonProperty("proxyBaseUrl")
    status = JsonProperty("status")
    status_message = JsonProperty("statusMessage")
    transformer_parameters = JsonProperty("transformerParameters", klass=dict)
    transformers = JsonProperty("transformers", klass=list)


class Mapping(BaseEntity):
    priority = JsonProperty("priority")
    request = JsonProperty("request", klass=MappingRequest)
    response = JsonProperty("response", klass=MappingResponse)
    persistent = JsonProperty("persistent")
    post_serve_actions = JsonProperty("postServeActions", klass=dict)
    new_scenario_state = JsonProperty("newScenarioState")
    required_scenario_state = JsonProperty("requiredScenarioState")
    scenario_name = JsonProperty("scenarioName")


@add_metaclass(BaseEntityMetaType)
class MappingMeta(BaseAbstractEntity):
    total = JsonProperty("total")


@add_metaclass(BaseEntityMetaType)
class AllMappings(BaseAbstractEntity):
    mappings = JsonProperty("mappings", klass=list, list_klass=Mapping)
    meta = JsonProperty("meta", klass=MappingMeta)


__all__ = [
    "Mapping",
    "MappingResponse",
    "MappingRequest",
    "DelayDistribution",
    "ResponseFaultType",
    "DelayDistributionMethods",
    "BasicAuthCredentials",
    "WireMockMatchers",
    "HttpMethods",
    "CommonHeaders",
    "MappingMeta",
    "AllMappings",
]
