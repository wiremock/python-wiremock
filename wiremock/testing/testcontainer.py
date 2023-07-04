import json
import os
import tarfile
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Optional
from urllib.parse import urljoin

import docker
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.exceptions import ContainerStartException
from testcontainers.core.waiting_utils import wait_container_is_ready

from wiremock.resources.mappings.models import Mapping

TMappingConfigs = dict[str | dict, str | int | dict | Mapping]


class WireMockContainer(DockerContainer):
    """
    Wiremock container.
    """

    MAPPINGS_DIR: str = "/home/wiremock/mappings/"
    FILES_DIR: str = "/home/wiremock/__files/"

    def __init__(
        self,
        image: str = "wiremock/wiremock:2.35.0",
        http_server_port: int = 8080,
        https_server_port: int = 8443,
        secure: bool = True,
        verify_ssl_certs: bool = True,
        init: bool = True,
        docker_client_kwargs: dict[str, Any] = {},
    ) -> None:
        self.http_server_port = http_server_port
        self.https_server_port = https_server_port
        self.secure = secure
        self.verify_ssl_certs = verify_ssl_certs
        super(WireMockContainer, self).__init__(image, **docker_client_kwargs)

        if init:
            self.initialize()

    def initialize(self) -> None:
        self.wire_mock_args: list[str] = []
        self.mapping_stubs: dict[str, str] = {}
        self.mapping_files: dict[str, str] = {}
        self.extensions: dict[str, bytes] = {}

        if self.secure:
            self.with_https_port()
        else:
            self.with_http_port()

    def with_http_port(self) -> None:
        self.with_cli_arg("--port", str(self.http_server_port))
        self.with_exposed_ports(self.http_server_port)

    def with_https_port(self) -> None:
        self.with_cli_arg("--https-port", str(self.https_server_port))
        self.with_exposed_ports(self.https_server_port)

    def with_cli_arg(self, arg_name: str, arg_value: str) -> "WireMockContainer":
        self.wire_mock_args.append(arg_name)
        self.wire_mock_args.append(arg_value)
        return self

    def with_mapping(self, name: str, data: TMappingConfigs) -> "WireMockContainer":
        self.mapping_stubs[name] = json.dumps(data)
        return self

    def with_file(self, name: str, data: dict[str, Any]):
        self.mapping_files[name] = json.dumps(data)
        return self

    def with_command(self, cmd: Optional[str] = None) -> "WireMockContainer":

        if not cmd:
            cmd = " ".join(self.wire_mock_args)

        super().with_command(cmd)

        return self

    def copy_file_to_container(self, host_path: Path, container_path: Path) -> None:
        with open(host_path, "rb") as fp:
            self.get_wrapped_container().put_archive(
                path=container_path, data=fp.read()
            )

    def copy_files_to_container(
        self, configs: dict[str, Any], container_dir_path: Path, mode: str = "w+"
    ) -> None:

        temp_dir = tempfile.mkdtemp()

        # generate temp files all config files
        for config_name, config_content in configs.items():
            file_name = os.path.basename(config_name)
            destination_path = os.path.join(temp_dir, file_name)
            with open(destination_path, mode) as fp:
                fp.write(config_content)

        # tar all files from temp dir
        tarfile_path = f"{temp_dir}.tar.gz"
        with tarfile.open(tarfile_path, "w:gz") as tar:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    tar.add(file_path, arcname=arcname)

        # copy tar archive onto container and extract at {container_dir_path}
        self.copy_file_to_container(
            host_path=Path(tarfile_path), container_path=container_dir_path
        )

    def copy_mappings_to_container(self) -> None:
        """Copies all mappings files generated with
        `.with_mapping('hello-world.json', {...})` to the container under
        the configured MAPPINGS_DIR
        """

        self.copy_files_to_container(
            configs=self.mapping_stubs, container_dir_path=Path(f"{self.MAPPINGS_DIR}")
        )

    def copy_mapping_files_to_container(self) -> None:
        """Copies all mappings files generated with
        `.with_file('hello.json', {...})` to the container under
        the configured FILES_DIR
        """
        self.copy_files_to_container(
            configs=self.mapping_files, container_dir_path=Path(f"{self.FILES_DIR}")
        )

    def server_running(self, retry_count: int = 3, retry_delay: int = 1) -> bool:
        """Pings the __admin/mappings endpoint of the wiremock server running inside the
        container as a proxy for checking if the server is up and running.

        {retry_count} attempts requests will be made with a delay of {retry_delay}
        to allow for race conditions when containers are being spun up
        quickly between tests.

        Args:
            retry_count: The number of attempts made to ping the server
            retry_delay: The number of seconds to wait before each attempt

        Returns:
            True if the request is successful
        """

        for _ in range(retry_count):
            try:
                response = requests.get(
                    self.get_url("__admin/mappings"), verify=self.verify_ssl_certs
                )
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")

            time.sleep(retry_delay)

        return False

    def reload_mappings(self) -> requests.Response:
        resp = requests.post(
            self.get_url("__admin/mappings/reset"), verify=self.verify_ssl_certs
        )
        if not resp.status_code <= 300:
            raise Exception("Failed to reload mappings")

        return resp

    @wait_container_is_ready()
    def configure(self) -> None:
        if not self.server_running():
            raise Exception("Server does not appear to be running in container")

        self.copy_mappings_to_container()
        self.copy_mapping_files_to_container()

        self.reload_mappings()

    def get_base_url(self) -> str:
        """Generate the base url of the container wiremock-server

        Returns:
            The base to the container based on the hostname and exposed ports
        """
        proto = "https" if self.secure else "http"
        port = self.https_server_port if self.secure else self.http_server_port
        return f"{proto}://{self.get_container_host_ip()}:{self.get_exposed_port(port)}"

    def get_url(self, path: str) -> str:
        return urljoin(self.get_base_url(), path)

    def start(self, cmd: Optional[str] = None) -> "WireMockContainer":
        self.with_command(cmd)
        super().start()
        self.configure()
        return self


@contextmanager
def wiremock_container(
    image: str = "wiremock/wiremock:2.35.0",
    http_server_port: int = 8080,
    https_server_port: int = 8443,
    secure: bool = True,
    verify_ssl_certs: bool = True,
    mappings: list[tuple[str, TMappingConfigs]] = [],
    start: bool = True,
    docker_client_kwargs: dict[str, Any] = {},
) -> Generator[WireMockContainer, None, None]:
    """
    Start a wiremock test container using Testcontainers

    :return: WireMockContainer instance
    """

    client = docker.from_env()
    client.ping()
    try:
        wm = WireMockContainer(
            image=image,
            http_server_port=http_server_port,
            https_server_port=https_server_port,
            secure=secure,
            verify_ssl_certs=verify_ssl_certs,
            docker_client_kwargs=docker_client_kwargs,
        )
        [wm.with_mapping(m_name, m_data) for m_name, m_data in mappings]
        if start:
            with wm:
                yield wm
        else:
            yield wm
    except ContainerStartException as e:
        raise Exception("Error starting wiremock container") from e
    except requests.exceptions.RequestException as e:
        raise Exception("Error connecting to wiremock container") from e
    finally:
        client.close()
