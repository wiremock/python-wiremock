# -*- coding: utf-8 -*-
"""TODO: Document base_resource_tests here.

Copyright (C) 2017, Auto Trader UK
Created 24. Apr 2017 15:42
Creator: john.harrison

"""

import unittest

from requests import Response

from wiremock.base import RestClient
from wiremock.exceptions import UnexpectedResponseException
from wiremock.tests import BaseClientTestCase


class RestClientTestCase(BaseClientTestCase):

    def setUp(self):
        super(RestClientTestCase, self).setUp()
        self.client = RestClient()

    def test_handle_response(self):
        for status_code in [200, 201, 204]:
            resp = self._create_dummy_response(status_code)
            returned = self.client.handle_response(resp)
            self.assertEqual(returned, resp)

        resp = self._create_dummy_response(203)
        with self.assertRaises(UnexpectedResponseException):
            self.client.handle_response(resp)

    # Helpers

    def _create_dummy_response(self, status_code=200):
        resp = Response()
        resp.status_code = status_code
        return resp


if __name__ == '__main__':
    unittest.main()
