from wiremock._compat import add_metaclass
from wiremock.base import JsonProperty, BaseAbstractEntity, BaseEntityMetaType


@add_metaclass(BaseEntityMetaType)
class GlobalSetting(BaseAbstractEntity):
    fixed_delay = JsonProperty("fixedDelay")


__all__ = ["GlobalSetting"]
