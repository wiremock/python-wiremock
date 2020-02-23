import json
import requests
from requests import exceptions as rexc

from wiremock.base.base_entity import BaseAbstractEntity
from wiremock.constants import make_headers, Config, logger
from wiremock.exceptions import *


class RestClient(object):
    def __init__(self, timeout=None, base_url=None, requests_verify=None, requests_cert=None):
        self.timeout = timeout
        self.base_url = base_url
        self.requests_verify = requests_verify
        self.requests_cert = requests_cert

    def _base_url(self):
        return self.base_url or Config.base_url

    def _timeout(self):
        return self.timeout or Config.timeout

    def _requests_verify(self):
        return self.requests_verify or Config.requests_verify

    def _requests_cert(self):
        return self.requests_cert or Config.requests_cert

    def _log(self, action, url, **kwargs):
        ctx = {"timeout": kwargs.get("timeout")}
        logger.debug("%s [%s] - %s", action, url, kwargs.get("json", json.dumps(kwargs.get("data", None))), extra=ctx)

    def post(self, uri, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("POST", url, **kwargs)
            return requests.post(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    def get(self, uri, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("GET", url, **kwargs)
            return requests.get(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    def put(self, uri, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("PUT", url, **kwargs)
            return requests.put(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    def patch(self, uri, **kwargs):  # pragma: no cover
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("PATCH", url, **kwargs)
            return requests.patch(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    def delete(self, uri, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("DELETE", url, **kwargs)
            return requests.delete(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    def options(self, uri, **kwargs):  # pragma: no cover
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("OPTIONS", url, **kwargs)
            return requests.options(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    def head(self, uri, **kwargs):  # pragma: no cover
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout()
        if "requests_verify" not in kwargs:
            kwargs["verify"] = self._requests_verify()
        if "requests_cert" not in kwargs:
            kwargs["cert"] = self._requests_cert()
        try:
            url = self._base_url() + uri
            self._log("HEAD", url, **kwargs)
            return requests.head(url, **kwargs)
        except rexc.Timeout as e:  # pragma: no cover
            raise TimeoutException(-1, e)
        except rexc.ConnectionError as e:  # pragma: no cover
            raise ApiUnavailableException(-1, e)

    @staticmethod
    def handle_response(response):
        sc = response.status_code
        if sc in [200, 201, 204]:
            return response
        elif sc is 401:  # pragma: no cover
            raise RequiresLoginException(sc, response.text)
        elif sc is 403:  # pragma: no cover
            raise ForbiddenException(sc, response.text)
        elif sc is 404:  # pragma: no cover
            raise NotFoundException(sc, response.text)
        elif sc is 422:  # pragma: no cover
            raise InvalidInputException(sc, response.text)
        elif 200 < sc < 400:  # pragma: no cover
            raise UnexpectedResponseException(sc, response.text)
        elif 400 <= sc < 500 and sc is not 404:  # pragma: no cover
            raise ClientException(sc, response.text)
        elif 500 <= sc < 600:  # pragma: no cover
            raise ServerException(sc, response.text)
        else:  # pragma: no cover
            raise ApiException(sc, response.text)


class BaseResource(object):

    REST_CLIENT = RestClient()

    @classmethod
    def endpoint(cls):
        return "/"  # pragma: no cover

    @classmethod
    def endpoint_single(cls):
        return "/{id}"  # pragma: no cover

    @classmethod
    def entity_class(cls):
        return None  # pragma: no cover

    @classmethod
    def get_base_uri(cls, endpoint, **id_dict):
        if id_dict:
            return endpoint.format(**id_dict)
        return endpoint

    @staticmethod
    def get_entity_id(entity_id, entityClass):
        if not (isinstance(entity_id, (int, str)) or isinstance(entity_id, entityClass)):
            raise InvalidInputException(422, entity_id)
        if isinstance(entity_id, entityClass):
            entity_id = entity_id.id

        return entity_id

    @staticmethod
    def validate_is_entity(entity, entityClass):
        if not isinstance(entity, entityClass):
            raise InvalidInputException(422, entity)

    @classmethod
    def _create(cls, entity, parameters=None, ids={}):  # pragma: no cover
        if isinstance(entity, BaseAbstractEntity):
            response = cls.REST_CLIENT.post(
                cls.get_base_uri(cls.endpoint(), **ids), json=entity.get_json_data(), headers=make_headers(), params=parameters
            )
        else:
            response = cls.REST_CLIENT.post(
                cls.get_base_uri(cls.endpoint(), **ids), data=json.dumps(entity), headers=make_headers(), params=parameters
            )

        response = cls.REST_CLIENT.handle_response(response)

        if cls.entity_class() is None or not issubclass(cls.entity_class(), BaseAbstractEntity):
            return response  # pragma: no cover
        else:
            return cls.entity_class().from_dict(response.json())

    @classmethod
    def _update(cls, entity, parameters=None, ids={}):  # pragma: no cover
        entity_id = getattr(entity, "id", None)
        if entity_id is not None:
            ids["id"] = entity_id
        if isinstance(entity, BaseAbstractEntity):
            response = cls.REST_CLIENT.put(
                cls.get_base_uri(cls.endpoint_single(), **ids), json=entity.get_json_data(), headers=make_headers(), params=parameters
            )
        else:
            response = cls.REST_CLIENT.put(
                cls.get_base_uri(cls.endpoint_single(), **ids), data=json.dumps(entity), headers=make_headers(), params=parameters
            )

        response = cls.REST_CLIENT.handle_response(response)

        if cls.entity_class() is None or not issubclass(cls.entity_class(), BaseAbstractEntity):
            return response  # pragma: no cover
        else:
            return cls.entity_class().from_dict(response.json())

    @classmethod
    def _partial_update(cls, entity, parameters=None, ids={}):  # pragma: no cover
        entity_id = getattr(entity, "id", None)
        if entity_id is not None:
            ids["id"] = entity_id
        if isinstance(entity, BaseAbstractEntity):
            response = cls.REST_CLIENT.patch(
                cls.get_base_uri(cls.endpoint_single(), **ids), json=entity.get_json_data(), headers=make_headers(), params=parameters
            )
        else:
            response = cls.REST_CLIENT.patch(
                cls.get_base_uri(cls.endpoint_single(), **ids), data=json.dumps(entity), headers=make_headers(), params=parameters
            )

        response = cls.REST_CLIENT.handle_response(response)

        if cls.entity_class() is None or not issubclass(cls.entity_class(), BaseAbstractEntity):
            return response  # pragma: no cover
        else:
            return cls.entity_class().from_dict(response.json())

    @classmethod
    def _retreive_all(cls, parameters=None, ids={}):  # pragma: no cover
        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint(), **ids), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)

        if cls.entity_class() is None or not issubclass(cls.entity_class(), BaseAbstractEntity):
            return response  # pragma: no cover
        else:
            response_json = response.json()
            if isinstance(response_json, (tuple, list)):
                results = []
                for r in response_json:
                    if isinstance(r, dict):
                        results.append(cls.entity_class().from_dict(r))
                return results
            else:
                return cls.entity_class().from_dict(response.json())

    @classmethod
    def _retreive_one(cls, entity, parameters=None, ids={}):  # pragma: no cover
        if isinstance(entity, (int, float)):
            ids["id"] = entity
            response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        elif entity is not None and issubclass(entity, BaseAbstractEntity):
            entity_id = getattr(entity, "id", None)
            ids["id"] = entity_id
            response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        else:
            response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)

        response = cls.REST_CLIENT.handle_response(response)

        if cls.entity_class() is None or not issubclass(cls.entity_class(), BaseAbstractEntity):
            return response  # pragma: no cover
        else:
            return cls.entity_class().from_dict(response.json())

    @classmethod
    def _delete(cls, entity, parameters=None, ids={}):  # pragma: no cover
        if isinstance(entity, (int, float)):
            ids["id"] = entity
            response = cls.REST_CLIENT.delete(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        elif isinstance(entity, BaseAbstractEntity):
            entity_id = getattr(entity, "id", None)
            ids["id"] = entity_id
            response = cls.REST_CLIENT.delete(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        else:
            response = cls.REST_CLIENT.delete(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)

        response = cls.REST_CLIENT.handle_response(response)
        if response is None:
            return entity

        if cls.entity_class() is None or not issubclass(cls.entity_class(), BaseAbstractEntity):
            return response  # pragma: no cover
        else:
            try:
                return cls.entity_class().from_dict(response.json())
            except ValueError:
                return response  # pragma: no cover


__all__ = ["RestClient", "BaseResource"]
