from wiremock._compat import add_metaclass
from wiremock.base import JsonProperty, BaseAbstractEntity, BaseEntityMetaType
from wiremock.resources.mappings.models import BasicAuthCredentials


@add_metaclass(BaseEntityMetaType)
class NearMissMatchRequest(BaseAbstractEntity):
    url = JsonProperty("url")
    absolute_url = JsonProperty("absoluteUrl")
    method = JsonProperty("method")
    client_ip = JsonProperty("clientIp")
    headers = JsonProperty("headers", klass=dict)
    query_parameters = JsonProperty("queryParameters", klass=dict)
    cookies = JsonProperty("cookies", klass=dict)
    basic_auth_credentials = JsonProperty("basicAuthCredentials", klass=BasicAuthCredentials)
    browser_proxy_request = JsonProperty("browserProxyRequest")  # type: bool
    body_as_base64 = JsonProperty("bodyAsBase64")
    body = JsonProperty("body")
    logged_date = JsonProperty("loggedDate")  # epoch seconds
    logged_date_string = JsonProperty("loggedDateString")


@add_metaclass(BaseEntityMetaType)
class NearMissMatchPatternRequest(BaseAbstractEntity):
    url = JsonProperty("url")
    url_pattern = JsonProperty("urlPattern")
    url_path = JsonProperty("urlPath")
    url_path_pattern = JsonProperty("urlPathPattern")
    method = JsonProperty("method")
    client_ip = JsonProperty("clientIp")
    headers = JsonProperty("headers", klass=dict)
    query_parameters = JsonProperty("queryParameters", klass=dict)
    cookies = JsonProperty("cookies", klass=dict)
    body_patterns = JsonProperty("bodyPatterns", klass=dict)
    basic_auth_credentials = JsonProperty("basicAuthCredentials", klass=BasicAuthCredentials)
    browser_proxy_request = JsonProperty("browserProxyRequest")  # type: bool
    logged_date = JsonProperty("loggedDate")  # epoch seconds
    logged_date_string = JsonProperty("loggedDateString")


# Responses


@add_metaclass(BaseEntityMetaType)
class NearMissRequestPatternResult(BaseAbstractEntity):
    url = JsonProperty("url")
    absolute_url = JsonProperty("absoluteUrl")
    method = JsonProperty("method")
    client_ip = JsonProperty("clientIp")
    headers = JsonProperty("headers", klass=dict)
    query_parameters = JsonProperty("queryParameters", klass=dict)
    cookies = JsonProperty("cookies", klass=dict)
    basic_auth_credentials = JsonProperty("basicAuthCredentials", klass=BasicAuthCredentials)
    browser_proxy_request = JsonProperty("browserProxyRequest")  # type: bool
    body_as_base64 = JsonProperty("bodyAsBase64")
    body = JsonProperty("body")


@add_metaclass(BaseEntityMetaType)
class NearMissMatchResult(BaseAbstractEntity):
    distance = JsonProperty("distance")  # type: float


@add_metaclass(BaseEntityMetaType)
class NearMissMatch(BaseAbstractEntity):
    request = JsonProperty("request", klass=NearMissMatchRequest)
    request_pattern = JsonProperty("requestPattern", klass=NearMissRequestPatternResult)
    match_result = JsonProperty("matchResult", klass=NearMissMatchResult)


@add_metaclass(BaseEntityMetaType)
class NearMissMatchResponse(BaseAbstractEntity):
    near_misses = JsonProperty("nearMisses", klass=list, list_klass=NearMissMatch)


__all__ = [
    "NearMissMatchResponse",
    "NearMissMatchRequest",
    "NearMissMatchResult",
    "NearMissRequestPatternResult",
    "NearMissMatch",
    "NearMissMatchPatternRequest",
]
