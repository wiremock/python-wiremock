# -*- coding: utf-8 -*-
"""Test wiremock.server."""

import unittest
from subprocess import STDOUT, PIPE

import responses
from mock import patch, DEFAULT
from pkg_resources import resource_filename

from wiremock.server.exceptions import WireMockServerAlreadyStartedError, WireMockServerNotStartedError
from wiremock.server.server import WireMockServer
from wiremock.tests.base import attr


class WireMockServerTestCase(unittest.TestCase):
    def setUp(self):
        self.java_path = "/path/to/java"
        self.jar_path = "/path/to/jar"
        self.port = 54321
        with patch.object(WireMockServer, "_get_free_port", return_value=self.port):
            self.wm = WireMockServer(java_path=self.java_path, jar_path=self.jar_path)

    @attr("unit", "server")
    def test_init(self):
        with patch.object(WireMockServer, "_get_free_port") as _get_free_port:
            _get_free_port.return_value = self.port

            wm = WireMockServer(java_path=self.java_path, jar_path=self.jar_path)

            self.assertEqual(wm.port, _get_free_port.return_value)

        self.assertEqual(wm.java_path, self.java_path)
        self.assertEqual(wm.jar_path, self.jar_path)
        self.assertFalse(wm.is_running)

    @attr("unit", "server")
    def test_init_with_defaults(self):
        with patch.object(WireMockServer, "_get_free_port", return_value=self.port):
            wm = WireMockServer()

        expected_jar = resource_filename("wiremock", "server/wiremock-standalone-2.6.0.jar")
        self.assertEqual(wm.java_path, "java")  # Assume java in PATH
        self.assertEqual(wm.jar_path, expected_jar)

    @attr("unit", "server")
    @patch("wiremock.server.server.socket")
    def test_get_free_port(self, mock_socket):
        sock = mock_socket.socket.return_value
        expected_port = 54321
        sock.getsockname.return_value = ("localhost", expected_port)

        port = self.wm._get_free_port()

        self.assertEqual(port, expected_port)

    @attr("unit", "server")
    @patch("wiremock.server.server.atexit")
    @patch("wiremock.server.server.Popen")
    @responses.activate
    def test_start(self, Popen, atexit):
        # mock healthy endpoint
        responses.add(responses.GET, "http://localhost:{}/__admin".format(self.wm.port), json=[], status=200)

        def poll():
            Popen.return_value.returncode = None
            return None

        Popen.return_value.poll.side_effect = poll

        self.wm.start()

        Popen.assert_called_once_with([self.java_path, "-jar", self.jar_path, "--port", str(54321)], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

        self.assertTrue(self.wm.is_running)
        atexit.register.assert_called_once_with(self.wm.stop, raise_on_error=False)

        # Test when already started
        with self.assertRaises(WireMockServerAlreadyStartedError):
            self.wm.start()

    @attr("unit", "server")
    def test_start_with_invalid_java(self):
        wm = WireMockServer(java_path="/no/such/path")
        with self.assertRaises(WireMockServerNotStartedError):
            wm.start()

    @attr("unit", "server")
    def test_start_with_invalid_jar(self):
        wm = WireMockServer(jar_path="/dev/null")
        with self.assertRaises(WireMockServerNotStartedError):
            wm.start()

    @attr("unit", "server")
    def test_stop(self):
        with patch.object(self.wm, "_WireMockServer__subprocess") as _subprocess:
            self.wm._WireMockServer__running = True

            self.wm.stop()

            _subprocess.kill.assert_called_once_with()

            # Test repeated call

            _subprocess.kill.side_effect = AttributeError
            with self.assertRaises(WireMockServerNotStartedError):
                self.wm.stop()

    @attr("unit", "server")
    def test_with_statement(self):
        with patch.multiple(WireMockServer, start=DEFAULT, stop=DEFAULT) as mocks:

            with WireMockServer() as wm:
                self.assertIsInstance(wm, WireMockServer)
                mocks["start"].assert_called_once_with()

            mocks["stop"].assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
