from wiremock.base.base_resource import BaseResource
from wiremock.resources.settings import GlobalSetting


class GlobalSettings(BaseResource):
    @classmethod
    def endpoint(cls):
        return "/settings"

    @classmethod
    def endpoint_single(cls):
        return "/settings"

    @classmethod
    def entity_class(cls):
        return GlobalSetting

    @classmethod
    def update_global_settings(cls, settings, parameters={}):
        return cls._create(settings, parameters=parameters)


__all__ = ["GlobalSettings"]
