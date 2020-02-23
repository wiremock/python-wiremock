from wiremock.constants import make_headers
from wiremock.base.base_resource import BaseResource
from wiremock.resources.requests import RequestCountResponse, RequestResponse, RequestResponseAll, RequestResponseFindResponse
from wiremock.resources.near_misses import NearMissMatchPatternRequest, NearMissMatchResponse


class Requests(BaseResource):
    @classmethod
    def endpoint(cls):
        return "/requests"

    @classmethod
    def endpoint_single(cls):
        return "/requests/{id}"

    @classmethod
    def endpoint_requests_unmatched(cls):
        return cls.endpoint() + "/unmatched"

    @classmethod
    def endpoint_request_unmatched_near_misses(cls):
        return cls.endpoint_requests_unmatched() + "/near-misses"

    @classmethod
    def entity_class(cls):
        return RequestResponse

    @classmethod
    def get_all_received_requests(cls, limit=None, since=None, parameters={}):
        if limit is not None and limit > 0:
            parameters["limit"] = limit
        if since is not None:
            parameters["since"] = since

        response = cls.REST_CLIENT.get(cls.endpoint(), params=parameters, headers=make_headers())
        response = cls.REST_CLIENT.handle_response(response)

        return RequestResponseAll.from_dict(response.json())

    @classmethod
    def get_request(cls, request_id, parameters={}):
        ids = {"id": request_id}
        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)
        return RequestResponse.from_dict(response.json())

    @classmethod
    def reset_request_journal(cls, parameters={}):
        ids = {"id": "reset"}
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        return cls.REST_CLIENT.handle_response(response)

    @classmethod
    def get_matching_request_count(cls, request, parameters={}):
        cls.validate_is_entity(request, NearMissMatchPatternRequest)
        ids = {"id": "count"}
        response = cls.REST_CLIENT.post(
            cls.get_base_uri(cls.endpoint_single(), **ids), json=request.get_json_data(), headers=make_headers(), params=parameters
        )
        response = cls.REST_CLIENT.handle_response(response)
        return RequestCountResponse.from_dict(response.json())

    @classmethod
    def get_matching_requests(cls, request, parameters={}):
        cls.validate_is_entity(request, NearMissMatchPatternRequest)
        ids = {"id": "find"}
        response = cls.REST_CLIENT.post(
            cls.get_base_uri(cls.endpoint_single(), **ids), json=request.get_json_data(), headers=make_headers(), params=parameters
        )
        response = cls.REST_CLIENT.handle_response(response)
        return RequestResponseFindResponse.from_dict(response.json())

    @classmethod
    def get_unmatched_requests(cls, parameters={}):
        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_requests_unmatched()), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)

        return RequestResponseFindResponse.from_dict(response.json())

    @classmethod
    def get_unmatched_requests_near_misses(cls, parameters={}):
        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_request_unmatched_near_misses()), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)
        return NearMissMatchResponse.from_dict(response.json())


__all__ = ["Requests"]
