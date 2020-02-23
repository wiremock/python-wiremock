from wiremock.base.base_resource import BaseResource
from wiremock.resources.near_misses import NearMissMatchPatternRequest, NearMissMatchRequest, NearMissMatchResponse


class NearMisses(BaseResource):
    @classmethod
    def endpoint(cls):
        return "/near-misses"

    @classmethod
    def endpoint_single(cls):
        return "/near-misses"

    @classmethod
    def endpoint_request(cls):
        return cls.endpoint() + "/request"

    @classmethod
    def endpoint_request_pattern(cls):
        return cls.endpoint() + "/request-pattern"

    @classmethod
    def entity_class(cls):
        return NearMissMatchResponse

    @classmethod
    def find_nearest_misses_by_request(cls, request, parameters={}):
        cls.validate_is_entity(request, NearMissMatchRequest)
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint_request()), json=request.get_json_data(), params=parameters)

        response = cls.REST_CLIENT.handle_response(response)
        return NearMissMatchResponse.from_dict(response.json())

    @classmethod
    def find_nearest_misses_by_request_pattern(cls, request_pattern, parameters={}):
        cls.validate_is_entity(request_pattern, NearMissMatchPatternRequest)
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint_request_pattern()), json=request_pattern.get_json_data(), params=parameters)

        response = cls.REST_CLIENT.handle_response(response)
        return NearMissMatchResponse.from_dict(response.json())


__all__ = ["NearMisses"]
