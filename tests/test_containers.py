from pathlib import Path
from typing import cast
from unittest.mock import Mock, patch

import requests
from docker.models.containers import Container

from wiremock.testing.testcontainer import WireMockContainer, wiremock_container


def test_get_secure_base_url():
    # Arrange
    with wiremock_container(verify_ssl_certs=False) as wm:
        host = wm.get_container_host_ip()
        port = wm.get_exposed_port(wm.https_server_port)
        expected_url = f"https://{host}:{port}"

        # Act/Assert
        assert wm.get_base_url() == expected_url


def test_get_secure_url():
    # Arrange
    with wiremock_container(verify_ssl_certs=False) as wm:
        path = "example-path"
        host = wm.get_container_host_ip()
        port = wm.get_exposed_port(wm.https_server_port)
        expected_url = f"https://{host}:{port}/example-path"

        # Act/Assert
        assert wm.get_url(path) == expected_url


def test_get_non_secure_base_url():
    # Arrange
    with wiremock_container(secure=False, verify_ssl_certs=False) as wm:
        host = wm.get_container_host_ip()
        port = wm.get_exposed_port(wm.http_server_port)
        expected_url = f"http://{host}:{port}"

        # Act/Assert
        assert wm.get_base_url() == expected_url


def test_get_non_secure_url():
    # Arrange
    with wiremock_container(secure=False, verify_ssl_certs=False) as wm:
        path = "example-path"
        host = wm.get_container_host_ip()
        port = wm.get_exposed_port(wm.http_server_port)
        expected_url = f"http://{host}:{port}/example-path"

        # Act/Assert
        assert wm.get_url(path) == expected_url


@patch.object(WireMockContainer, "initialize")
def test_initialize_method_call_on_instance_creation(mock_init):

    # Arrange/Act
    WireMockContainer()

    # Assert
    mock_init.assert_called_once_with()


@patch.object(WireMockContainer, "with_https_port")
def test_initialize_set_defaults(mock_set_secure_port):

    wm = WireMockContainer()

    assert wm.https_server_port == 8443
    assert wm.http_server_port == 8080
    assert wm.wire_mock_args == []
    assert wm.mapping_stubs == {}
    assert wm.mapping_files == {}
    assert wm.extensions == {}
    mock_set_secure_port.assert_called_once_with()


@patch.object(WireMockContainer, "with_http_port")
@patch.object(WireMockContainer, "with_https_port")
def test_initialize_non_secure_mode_sets_http_port(
    mock_set_secure_port, mock_set_unsecure_port
):
    wm = WireMockContainer(secure=False)

    assert wm.https_server_port == 8443
    assert wm.http_server_port == 8080
    assert wm.wire_mock_args == []
    assert wm.mapping_stubs == {}
    assert wm.mapping_files == {}
    assert wm.extensions == {}

    assert not mock_set_secure_port.called
    mock_set_unsecure_port.assert_called_once_with()


@patch.object(WireMockContainer, "with_exposed_ports")
@patch.object(WireMockContainer, "with_cli_arg")
def test_with_https_port_default(mock_cli_arg, mock_expose_port):

    # Arrange
    wm = WireMockContainer(init=False)

    # Act
    wm.with_https_port()

    # Assert
    mock_cli_arg.assert_called_once_with("--https-port", "8443")
    mock_expose_port.assert_called_once_with(wm.https_server_port)


@patch.object(WireMockContainer, "with_exposed_ports")
@patch.object(WireMockContainer, "with_cli_arg")
def test_with_https_port_with_user_defined_port_value(mock_cli_arg, mock_expose_port):

    # Arrange
    wm = WireMockContainer(https_server_port=9443, init=False)

    # Act
    wm.with_https_port()

    # Assert
    mock_cli_arg.assert_called_once_with("--https-port", "9443")
    mock_expose_port.assert_called_once_with(9443)


@patch.object(WireMockContainer, "with_exposed_ports")
@patch.object(WireMockContainer, "with_cli_arg")
def test_with_http_port_default(mock_cli_arg, mock_expose_port):

    # Arrange
    wm = WireMockContainer(init=False)

    # Act
    wm.with_http_port()

    # Assert
    mock_cli_arg.assert_called_once_with("--port", "8080")
    mock_expose_port.assert_called_once_with(wm.http_server_port)


@patch.object(WireMockContainer, "with_exposed_ports")
@patch.object(WireMockContainer, "with_cli_arg")
def test_with_http_port_with_user_defined_port_value(mock_cli_arg, mock_expose_port):

    # Arrange
    wm = WireMockContainer(http_server_port=5000, init=False)

    # Act
    wm.with_http_port()

    # Assert
    mock_cli_arg.assert_called_once_with("--port", "5000")
    mock_expose_port.assert_called_once_with(5000)


def test_container_starts_with_custom_https_port():

    # Arrange
    wm = WireMockContainer(verify_ssl_certs=False, https_server_port=9443)

    # Act
    with wm:

        assert wm.server_running() is True


def test_container_starts_with_custom_http_port():

    # Arrange
    wm = WireMockContainer(verify_ssl_certs=False, secure=False, http_server_port=5000)

    # Act
    with wm:

        assert wm.server_running() is True


def test_container_with_cli_arg_sets_cmd_line_args():

    # Arrange
    wm = WireMockContainer()

    # Act
    wm.with_cli_arg("--foo", "bar")

    # Assert
    assert wm.wire_mock_args == ["--https-port", "8443", "--foo", "bar"]


def test_container_with_command_generates_command_from_cli_args():

    # Arrange
    wm = WireMockContainer()

    # Act
    wm.with_command()

    # Assert
    assert wm._command == "--https-port 8443"


def test_container_with_command_override():

    # Arrange
    wm = WireMockContainer()

    # Act
    wm.with_command(cmd="--foo bar")

    # Assert
    assert wm._command == "--foo bar"


@patch.object(WireMockContainer, "get_wrapped_container", spec=Container)
def test_copy_file_to_container(mock_get_container: Mock, tmp_path: Path):

    # Arrange
    d = tmp_path / "mappings"
    d.mkdir()
    mapping = d / "mapping.json"
    mapping.write_text('{"foo": "bar"}')
    wm = WireMockContainer()

    # Act
    wm.copy_file_to_container(mapping, Path(wm.MAPPINGS_DIR))

    # Assert
    mock_get_container.return_value.put_archive.assert_called_once_with(
        path=Path(wm.MAPPINGS_DIR), data=b'{"foo": "bar"}'
    )


def test_configure_manually():

    wm = cast(
        WireMockContainer,
        (
            WireMockContainer(verify_ssl_certs=False)
            .with_mapping(
                "hello-world.json",
                {
                    "request": {"method": "GET", "url": "/hello"},
                    "response": {"status": 200, "body": "hello"},
                },
            )
            .with_mapping(
                "hello-world-file.json",
                {
                    "request": {"method": "GET", "url": "/hello2"},
                    "response": {"status": 200, "bodyFileName": "hello.json"},
                },
            )
            .with_file("hello.json", {"message": "Hello World !"})
            .with_cli_arg("--verbose", "")
            .with_cli_arg("--root-dir", "/home/wiremock")
            .with_env("JAVA_OPTS", "-Djava.net.preferIPv4Stack=true")
        ),
    )
    with wm:
        resp1 = requests.get(wm.get_url("/hello"), verify=False)
        resp2 = requests.get(wm.get_url("/hello2"), verify=False)
        assert resp1.status_code == 200
        assert resp1.content == b"hello"
        assert resp2.status_code == 200
        assert resp2.content == b'{"message": "Hello World !"}'
