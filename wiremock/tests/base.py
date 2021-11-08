import json
import logging
from nose.tools import nottest
from nose.plugins.attrib import attr
import responses
from unittest import TestCase

from wiremock.constants import Config


logging.basicConfig(level=logging.DEBUG)


class BaseClientTestCase(TestCase):
    """
    Adds utility methods.
    """

    @classmethod
    def setUpClass(cls):
        Config.base_url = "http://localhost/__admin"
        Config.timeout = 1
        super(BaseClientTestCase, cls).setUpClass()

    def assertHasAttr(self, obj, attr):
        self.assertTrue(hasattr(obj, attr), "%s doesn't have attribute: %s" % (obj, attr))

    def assertNotHasAttr(self, obj, attr):
        self.assertFalse(hasattr(obj, attr), "%s shouldn't have attribute: %s" % (obj, attr))

    def assertAttrEqual(self, obj, attr, value):
        self.assertHasAttr(obj, attr)
        self.assertEqual(getattr(obj, attr), value)

    def assertAttrNotEqual(self, obj, attr, value):
        self.assertHasAttr(obj, attr)
        self.assertNotEqual(getattr(obj, attr), value)

    def assertNotRaise(self, callableObj, *args, **kwargs):
        try:
            callableObj(*args, **kwargs)
        except Exception as e:
            raise AssertionError("Shouldn't raise and exception: {}".format(e))

    def assertAnyRaise(self, callableObj, *args, **kwargs):
        try:
            callableObj(*args, **kwargs)
        except:
            return
        raise AssertionError("Should raise an exception")

    def assertIsSubclass(self, C, B):
        if issubclass(C, B):
            return
        else:
            raise AssertionError("{} is Not a Subclass of {}".format(B, C))

    def assertDictContainsKey(self, obj, key):
        if key in obj:
            return
        else:
            raise AssertionError("{} is not in dict: {}".format(key, obj))

    def assertDictContainsKeyWithValue(self, obj, key, value):
        if key in obj:
            self.assertEqual(value, obj[key])
        else:
            raise AssertionError("{} is not in dict: {}".format(key, obj))

    def assertDictContainsKeyWithValueType(self, obj, key, B):
        if key in obj:
            if isinstance(obj[key], B):
                return
            else:
                raise AssertionError("dict[{}]={} is not of type: {}".format(key, obj[key], B))
        else:
            raise AssertionError("{} is not in dict: {}".format(key, obj))


__all__ = ["BaseClientTestCase", "nottest", "attr", "json", "responses"]
