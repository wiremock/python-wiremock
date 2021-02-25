from wiremock.constants import make_headers
from wiremock.base.base_resource import BaseResource
from wiremock.resources.mappings import Mapping, AllMappings, MappingResponse


class Mappings(BaseResource):
    @classmethod
    def endpoint(cls):
        return "/mappings"

    @classmethod
    def endpoint_single(cls):
        return "/mappings/{id}"

    @classmethod
    def endpoint_delete_by_metadata(cls):
        return "/mappings/remove-by-metadata"

    @classmethod
    def entity_class(cls):
        return MappingResponse

    @classmethod
    def create_mapping(cls, mapping, parameters={}):
        cls.validate_is_entity(mapping, Mapping)
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint()), json=mapping.get_json_data(), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)
        return MappingResponse.from_dict(response.json())

    @classmethod
    def retrieve_all_mappings(cls, parameters={}):
        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint()), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)
        return AllMappings.from_dict(response.json())

    @classmethod
    def retrieve_mapping(cls, mapping_id, parameters={}):
        mapping_id = cls.get_entity_id(mapping_id, Mapping)
        ids = {"id": mapping_id}
        response = cls.REST_CLIENT.get(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        response = cls.REST_CLIENT.handle_response(response)
        return Mapping.from_dict(response.json())

    @classmethod
    def update_mapping(cls, mapping, parameters={}):
        cls.validate_is_entity(mapping, Mapping)
        mapping_id = cls.get_entity_id(mapping, Mapping)
        ids = {"id": mapping_id}
        response = cls.REST_CLIENT.put(
            cls.get_base_uri(cls.endpoint_single(), **ids), json=mapping.get_json_data(), headers=make_headers(), params=parameters
        )
        response = cls.REST_CLIENT.handle_response(response)
        return Mapping.from_dict(response.json())

    @classmethod
    def persist_mappings(cls, parameters={}):
        ids = {"id": "save"}
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        return cls.REST_CLIENT.handle_response(response)

    @classmethod
    def reset_mappings(cls, parameters={}):
        ids = {"id": "reset"}
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        return cls.REST_CLIENT.handle_response(response)

    @classmethod
    def delete_all_mappings(cls, parameters={}):
        response = cls.REST_CLIENT.delete(cls.get_base_uri(cls.endpoint()), headers=make_headers(), params=parameters)
        return cls.REST_CLIENT.handle_response(response)

    @classmethod
    def delete_mapping(cls, mapping_id, parameters={}):
        mapping_id = cls.get_entity_id(mapping_id, Mapping)
        ids = {"id": mapping_id}
        response = cls.REST_CLIENT.delete(cls.get_base_uri(cls.endpoint_single(), **ids), headers=make_headers(), params=parameters)
        return cls.REST_CLIENT.handle_response(response)

    @classmethod
    def delete_mapping_by_metadata(cls, metadata, parameters={}):
        response = cls.REST_CLIENT.post(cls.get_base_uri(cls.endpoint_delete_by_metadata()), headers=make_headers(), params=parameters, json=metadata)

        return cls.REST_CLIENT.handle_response(response)


__all__ = ["Mappings"]
