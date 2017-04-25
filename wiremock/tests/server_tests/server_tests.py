# -*- coding: utf-8 -*-
"""TODO: Document server_tests here.

Copyright (C) 2017, Auto Trader UK
Created 25. Apr 2017 12:32
Creator: john.harrison

"""

import unittest
from mock import patch
from pkg_resources import resource_filename

from wiremock.server.server import WireMockServer


class WireMockServerTestCase(unittest.TestCase):

    def setUp(self):
        self.java_path = '/path/to/java'
        self.jar_path = '/path/to/jar'
        self.port = 54321
        with patch.object(WireMockServer, '_get_free_port', return_value=self.port):
            self.wm = WireMockServer(
                java_path=self.java_path,
                jar_path=self.jar_path
            )

    def test_init(self):
        with patch.object(WireMockServer, '_get_free_port') as _get_free_port:
            _get_free_port.return_value = self.port

            wm = WireMockServer(java_path=self.java_path, jar_path=self.jar_path)

            self.assertEqual(wm.port, _get_free_port.return_value)

        self.assertEqual(wm.java_path, self.java_path)
        self.assertEqual(wm.jar_path, self.jar_path)
        self.assertFalse(wm.is_running)

    def test_init_with_defaults(self):
        with patch.object(WireMockServer, '_get_free_port', return_value=self.port):
            wm = WireMockServer()

        expected_jar = resource_filename(
            'wiremock',
            'server/wiremock-standalone-2.6.0.jar'
        )
        self.assertEqual(wm.java_path, 'java')  # Assume java in PATH
        self.assertEqual(wm.jar_path, expected_jar)

    @patch('wiremock.server.server.socket')
    def test_get_free_port(self, mock_socket):
        sock = mock_socket.socket.return_value
        expected_port = 54321
        sock.getsockname.return_value = ('localhost', expected_port)

        port = self.wm._get_free_port()

        self.assertEqual(port, expected_port)


if __name__ == '__main__':
    unittest.main()
