from wiremock._compat import add_metaclass
from wiremock.base import BaseEntity, JsonProperty, BaseAbstractEntity, BaseEntityMetaType
from wiremock.resources.mappings.models import BasicAuthCredentials


@add_metaclass(BaseEntityMetaType)
class RequestCountResponse(BaseAbstractEntity):
    count = JsonProperty("count")


@add_metaclass(BaseEntityMetaType)
class RequestResponseRequest(BaseAbstractEntity):
    method = JsonProperty("method")
    url = JsonProperty("url")
    absolute_url = JsonProperty("absoluteUrl")
    client_ip = JsonProperty("clientIp")
    basic_auth_credentials = JsonProperty("basicAuthCredentials", klass=BasicAuthCredentials)
    cookies = JsonProperty("cookies", klass=dict)
    headers = JsonProperty("headers", klass=dict)
    query_parameters = JsonProperty("queryParameters", klass=dict)
    browser_proxy_request = JsonProperty("browserProxyRequest")  # should be true/false
    body = JsonProperty("body")
    body_as_base64 = JsonProperty("bodyAsBase64")
    logged_date = JsonProperty("loggedDate")  # epoch seconds
    logged_date_string = JsonProperty("loggedDateString")


@add_metaclass(BaseEntityMetaType)
class RequestResponseDefinition(BaseAbstractEntity):
    status = JsonProperty("status")
    transformers = JsonProperty("transformers", klass=list)
    from_configured_stub = JsonProperty("fromConfiguredStub")  # will be true/false
    transformer_parameters = JsonProperty("transformerParameters", klass=dict)


class RequestResponse(BaseEntity):
    request = JsonProperty("request", klass=RequestResponseRequest)
    response_definition = JsonProperty("responseDefinition", klass=RequestResponseDefinition)


@add_metaclass(BaseEntityMetaType)
class RequestResponseAllMeta(BaseAbstractEntity):
    total = JsonProperty("total")


@add_metaclass(BaseEntityMetaType)
class RequestResponseFindResponse(BaseAbstractEntity):
    requests = JsonProperty("requests", klass=list, list_klass=RequestResponseRequest)


@add_metaclass(BaseEntityMetaType)
class RequestResponseAll(BaseAbstractEntity):
    requests = JsonProperty("requests", klass=list, list_klass=RequestResponse)
    meta = JsonProperty("meta", klass=RequestResponseAllMeta)
    request_journal_disabled = JsonProperty("requestJournalDisabled")  # should be true/false


__all__ = [
    "RequestResponse",
    "RequestResponseDefinition",
    "RequestResponseRequest",
    "RequestCountResponse",
    "RequestResponseAll",
    "RequestResponseFindResponse",
    "RequestResponseAllMeta",
]
