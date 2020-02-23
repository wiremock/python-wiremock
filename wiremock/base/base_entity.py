from collections import OrderedDict
import json

from wiremock._compat import add_metaclass


class JsonPropertyValueContainer(object):
    def __init__(self, json_property, value):
        self.json_property = json_property
        self.value = value

    def getval(self):
        return self.value

    def setval(self, value):
        self.value = value

    def delval(self):  # pragma: no cover
        self.value = None

    def get_property(self):  # pragma: no cover
        _get = lambda slf: self.getval()
        _set = lambda slf, val: self.setval(val)
        _del = lambda slf: self.delval()

        return property(_get, _set, _del)


class JsonProperty(object):

    value_container = JsonPropertyValueContainer

    def __init__(self, json_name, property_name=None, klass=None, list_klass=None, dict_key_klass=None, dict_value_klass=None, include_if_null=False):
        self._json_name = json_name
        self._property_name = property_name
        self._klass = klass

        if self._klass is not None and not issubclass(self._klass, BaseAbstractEntity):
            if issubclass(self._klass, list) or issubclass(self._klass, tuple):
                self._list_klass = list_klass
            else:
                self._list_klass = None

            if issubclass(self._klass, dict):
                self._dict_key_klass = dict_key_klass
                self._dict_value_klass = dict_value_klass
            else:
                self._dict_key_klass = None
                self._dict_value_klass = None
        else:
            self._list_klass = None
            self._dict_key_klass = None
            self._dict_value_klass = None

        self._include_if_null = include_if_null

    def set_property_name(self, property_name):
        self._property_name = property_name
        if self._json_name is None:  # pragma: no cover
            self._json_name = self._property_name

    @property
    def json_name(self):
        return self._json_name

    @property
    def property_name(self):
        return self._property_name

    @property
    def klass(self):
        return self._klass

    @property
    def list_klass(self):
        return self._list_klass

    @property
    def dict_key_klass(self):
        return self._dict_key_klass

    @property
    def dict_value_klass(self):
        return self._dict_value_klass

    def is_dict(self):
        return self._klass is not None and issubclass(self._klass, dict)

    def is_list(self):
        return self._klass is not None and (issubclass(self._klass, list) or issubclass(self._klass, tuple))

    def is_base_entity_class(self):
        return self._klass is not None and issubclass(self._klass, BaseAbstractEntity)

    @property
    def include_if_null(self):
        return self._include_if_null

    def __str__(self):
        return "JsonProperty(json_name={}, property_name={}, klass={}, include_if_null={})".format(
            self._json_name, self._property_name, self._klass, self._include_if_null
        )

    def __unicode__(self):
        return "JsonProperty(json_name={}, property_name={}, klass={}, include_if_null={})".format(
            self._json_name, self._property_name, self._klass, self._include_if_null
        )


class EntityModelException(Exception):
    pass


class BaseAbstractEntity(object):
    """
    The base abstract entity class, don't inherit from this, inherit from BaseEntity, defined below.
    """

    def __init__(self, **values):
        self._values = {}
        for name, prop in self._properties.items():
            value = values.get(prop.json_name, values.get(name, None))
            if prop.is_list() and isinstance(value, (tuple, list)):  # This is a list with sub types
                l = prop.klass()
                for v in value:
                    if prop.list_klass is not None and issubclass(prop.list_klass, BaseAbstractEntity):
                        l.append(prop.list_klass.from_dict(v))
                    else:
                        l.append(v)
                value = l
                value_container = prop.value_container(prop, l)
            elif prop.is_dict() and isinstance(value, dict):  # This is a dict with sub types
                d = {}
                for k, v in value.items():
                    rk = k
                    rv = v

                    if prop.dict_key_klass is None:
                        pass
                    elif issubclass(prop.dict_key_klass, BaseAbstractEntity):
                        rk = prop.dict_key_klass.from_dict(k)
                    else:
                        rk = prop.dict_key_klass(k)

                    if prop.dict_value_klass is None:
                        pass
                    elif issubclass(prop.dict_value_klass, BaseAbstractEntity):
                        rv = prop.dict_value_klass.from_dict(v)
                    else:
                        rv = prop.dict_value_klass(v)

                    d[rk] = rv
                value = d
                value_container = prop.value_container(prop, d)
            elif prop.is_base_entity_class() and isinstance(value, dict):  # This is a BaseAbstractEntity Class
                value = prop.klass.from_dict(value)
                value_container = prop.value_container(prop, value)
            else:
                value_container = prop.value_container(prop, value)
            self._values[name] = value_container
            setattr(self, name, value)

    def __eq__(self, other):
        if not isinstance(other, BaseAbstractEntity):  # pragma: no cover
            return False

        return self.get_json_data() == other.get_json_data()

    def __ne__(self, other):  # pragma: no cover
        return not self.__eq__(other)

    @classmethod
    def from_json(cls, json_string):
        return cls(**json.loads(json_string))

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)

    def get_json_data(self):
        """
        Get the Dict of the properties

        :return: dict of properties
        """
        result = {}
        for name, prop in self._properties.items():
            item = getattr(self, name, None)
            if item is not None:
                if isinstance(item, BaseAbstractEntity):
                    item = item.get_json_data()
                elif isinstance(item, (tuple, list)):
                    tmp = []
                    for i in item:
                        if isinstance(i, BaseAbstractEntity):
                            tmp.append(i.get_json_data())
                        else:
                            tmp.append(i)
                    item = tmp
                elif isinstance(item, dict):
                    tmp = {}
                    for k, v in item.items():
                        if isinstance(v, BaseAbstractEntity):
                            tmp[k] = v.get_json_data()
                        else:
                            tmp[k] = v
                    item = tmp
            if item is not None or prop.include_if_null:
                result[prop.json_name] = item
        return result

    def to_json(self):
        """

        :return: json string of the data
        """
        return json.dumps(self.get_json_data())

    def __getitem__(self, item):
        value = self._properties.get(item, None)
        if value is not None:
            return getattr(self, item)
        raise AttributeError(item)

    def __setitem__(self, key, value):
        prop = self._properties.get(key)
        if prop is not None:
            setattr(key, value)

    def __delitem__(self, key):
        prop = self._properties.get(key)
        if prop is not None:
            delattr(self, key)
        else:
            raise AttributeError(key)

    def __contains__(self, item):
        return item in self._properties.keys()

    def __len__(self):
        return len(self._properties)

    def __iter__(self):
        for item in self._properties.keys():
            yield item

    def items(self):
        items = []
        for key in self._properties.keys():
            items.append((key, getattr(self, key)))
        return items

    def keys(self):
        return self._properties.keys()

    def values(self):
        items = []
        for key in self._properties.keys():
            items.append(getattr(self, key))
        return items


class BaseEntityMetaType(type):
    def __new__(mcs, name, bases, body):
        prop_dict = OrderedDict()

        for base in bases:
            for k, v in getattr(base, "_properties", {}).items():
                prop_dict.setdefault(k, v)

        def _transform_property(prop_name, prop_obj):
            prop_dict[prop_name] = prop_obj
            prop_obj.set_property_name(prop_name)
            _get = lambda self: self._values[prop_name].getval()
            _set = lambda self, val: self._values[prop_name].setval(val)
            _del = lambda self: self._values[prop_name].delval()
            body[prop_name] = property(_get, _set, _del)

        property_definitions = [(k, v) for k, v in body.items() if isinstance(v, JsonProperty)]

        for k, v in property_definitions:
            _transform_property(k, v)

        json_names = set()
        for v in prop_dict.values():
            # type: v -> EntityProperty
            if v.json_name in json_names:
                raise EntityModelException("%s defines the json property %s more than once" % (name, v.json_name))
            json_names.add(v.json_name)

        body["_properties"] = prop_dict

        # Create the class
        klass = super(BaseEntityMetaType, mcs).__new__(mcs, name, bases, body)

        return klass


def collection_to_json(collection):
    result = []
    for item in collection:
        if isinstance(item, BaseAbstractEntity):
            result.append(item.get_json_data())
        elif isinstance(item, (list, tuple)):
            sub_result = []
            for sub_item in item:
                if isinstance(sub_item, BaseAbstractEntity):
                    sub_result.append(sub_item.get_json_data())
            result.append(sub_result)
        elif isinstance(item, dict):
            sub_result = {}
            for k, v in item:
                if isinstance(v, BaseAbstractEntity):
                    sub_result[k] = v.get_json_data()
            result.append(sub_result)

    return json.dumps(result)


@add_metaclass(BaseEntityMetaType)
class BaseEntity(BaseAbstractEntity):
    _id = None

    def __init__(self, **values):
        self._id = values.pop("id", None)
        super(BaseEntity, self).__init__(**values)

    @property
    def id(self):
        """ Get the Id of the entity

        :return: id of entity
        """
        return self._id

    def __eq__(self, other):
        if not isinstance(other, BaseAbstractEntity):  # pragma: no cover
            return False

        return self._id == other.id

    def __ne__(self, other):  # pragma: no cover
        return not self.__eq__(other)

    def get_json_data(self):
        """
        Get the Dict of the properties

        :return: dict of properties
        """
        result = {}
        for name, prop in self._properties.items():
            item = getattr(self, name, None)
            if item is not None:
                if isinstance(item, BaseAbstractEntity):
                    item = item.get_json_data()
                elif item is not None and isinstance(item, (tuple, list)):
                    tmp = []
                    for i in item:
                        if isinstance(i, BaseAbstractEntity):
                            tmp.append(i.get_json_data())
                        else:
                            tmp.append(i)
                    item = tmp
                elif item is not None and isinstance(item, dict):
                    tmp = {}
                    for k, v in item.items():
                        if isinstance(v, BaseAbstractEntity):
                            tmp[k] = v.get_json_data()
                        else:
                            tmp[k] = v
                    item = tmp
            if item is not None or prop.include_if_null:
                result[prop.json_name] = item
        if self.id is not None:
            result["id"] = self.id
        return result


__all__ = ["BaseEntity", "BaseAbstractEntity", "BaseEntityMetaType", "collection_to_json", "EntityModelException", "JsonProperty"]
