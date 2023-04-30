from dataclasses import dataclass
from subprocess import PIPE, STDOUT
from unittest.mock import DEFAULT, patch

import pytest
import responses
from importlib_resources import files

from tests.utils import assertEqual, assertIsInstance
from wiremock.server.exceptions import (
    WireMockServerAlreadyStartedError,
    WireMockServerNotStartedError,
)
from wiremock.server.server import WireMockServer


@pytest.fixture()
def config():
    @dataclass
    class ServerConfig:

        java_path: str
        jar_path: str
        port: int

    return ServerConfig(
        java_path="/path/to/java",
        jar_path="/path/to/jar",
        port=54321,
    )


@pytest.fixture(scope="function")
def server(config):
    with patch.object(WireMockServer, "_get_free_port", return_value=config.port):
        yield WireMockServer(java_path=config.java_path, jar_path=config.jar_path)


@pytest.mark.usefixtures("server")
def test_init(config):
    with patch.object(WireMockServer, "_get_free_port") as _get_free_port:
        _get_free_port.return_value = config.port

        wm = WireMockServer(java_path=config.java_path, jar_path=config.jar_path)

        assertEqual(wm.port, _get_free_port.return_value)

    assertEqual(wm.java_path, config.java_path)
    assertEqual(wm.jar_path, config.jar_path)
    assert not wm.is_running


def test_init_with_defaults(config):
    with patch.object(WireMockServer, "_get_free_port", return_value=config.port):
        wm = WireMockServer()

    expected_jar = files("wiremock") / "server" / "wiremock-standalone-2.6.0.jar"
    assertEqual(wm.java_path, "java")  # Assume java in PATH
    assertEqual(wm.jar_path, expected_jar)


@patch("wiremock.server.server.socket")
def test_get_free_port(mock_socket, server):
    sock = mock_socket.socket.return_value
    expected_port = 54321
    sock.getsockname.return_value = ("localhost", expected_port)

    port = server._get_free_port()

    assertEqual(port, expected_port)


@patch("wiremock.server.server.atexit")
@patch("wiremock.server.server.Popen")
@responses.activate
def test_start(Popen, atexit, config, server):
    # mock healthy endpoint
    responses.add(
        responses.GET,
        "http://localhost:{}/__admin".format(server.port),
        json=[],
        status=200,
    )

    def poll():
        Popen.return_value.returncode = None
        return None

    Popen.return_value.poll.side_effect = poll

    server.start()

    Popen.assert_called_once_with(
        [
            config.java_path,
            "-jar",
            config.jar_path,
            "--port",
            str(54321),
            "--local-response-templating",
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
    )

    assert server.is_running is True
    atexit.register.assert_called_once_with(server.stop, raise_on_error=False)

    # Test when already started
    with pytest.raises(WireMockServerAlreadyStartedError):
        server.start()


def test_start_with_invalid_java():
    wm = WireMockServer(java_path="/no/such/path")
    with pytest.raises(WireMockServerNotStartedError):
        wm.start()


def test_start_with_invalid_jar():
    wm = WireMockServer(jar_path="/dev/null")
    with pytest.raises(WireMockServerNotStartedError):
        wm.start()


def test_stop(server):
    with patch.object(server, "_WireMockServer__subprocess") as _subprocess:
        server._WireMockServer__running = True

        server.stop()

        _subprocess.kill.assert_called_once_with()

        # Test repeated call

        _subprocess.kill.side_effect = AttributeError
        with pytest.raises(WireMockServerNotStartedError):
            server.stop()


def test_with_statement():
    with patch.multiple(WireMockServer, start=DEFAULT, stop=DEFAULT) as mocks:

        with WireMockServer() as wm:
            assertIsInstance(wm, WireMockServer)
            mocks["start"].assert_called_once_with()

        mocks["stop"].assert_called_once_with()
