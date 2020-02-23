from wiremock.constants import make_headers
from wiremock.base.base_resource import BaseResource


class Scenarios(BaseResource):
    @classmethod
    def endpoint(cls):
        return "/scenarios/reset"

    @classmethod
    def endpoint_single(cls):
        return "/scenarios"

    @classmethod
    def entity_class(cls):
        return None

    @classmethod
    def reset_all_scenarios(cls, parameters={}):
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint()), headers=make_headers(), params=parameters)
        return cls.REST_CLIENT.handle_response(response)


__all__ = ["Scenarios"]
