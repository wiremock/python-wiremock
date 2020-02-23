# -*- coding: utf-8 -*-
"""Tests for base_resource module."""

import unittest

from requests import Response

from wiremock.base import RestClient
from wiremock.exceptions import UnexpectedResponseException
from wiremock.tests.base import BaseClientTestCase, attr


class RestClientTestCase(BaseClientTestCase):
    def setUp(self):
        super(RestClientTestCase, self).setUp()
        self.client = RestClient()

    @attr("unit")
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


if __name__ == "__main__":
    unittest.main()
