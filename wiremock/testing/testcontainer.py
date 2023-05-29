import json
import os
import tarfile
import tempfile
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict
from urllib.parse import urljoin

import docker
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.exceptions import ContainerStartException
from testcontainers.core.waiting_utils import wait_container_is_ready


class WireMockContainer(DockerContainer):
    """
    Wiremock container.
    """

    DEFAULT_IMAGE_NAME: str = "wiremock/wiremock"
    DEFAULT_TAG: str = "latest"
    MAPPINGS_DIR: str = "/home/wiremock/mappings/"
    FILES_DIR: str = "/home/wiremock/__files/"
    EXTENSIONS_DIR: str = "/var/wiremock/extensions/"

    def __init__(
        self, image: str = "wiremock/wiremock", port: int = 8080, **kwargs
    ) -> None:
        self.port = port
        super(WireMockContainer, self).__init__(image, **kwargs)
        self.with_volume_mapping("/var/run/docker.sock", "/var/run/docker.sock")
        self.with_env("JAVA_OPTS", "-Djava.net.preferIPv4Stack=true")
        self.wire_mock_args: list[str] = []
        self.mapping_stubs: dict[str, str] = {}
        self.mapping_files: dict[str, str] = {}
        self.extensions: dict[str, bytes] = {}

    def with_env(self, key: str, value: str) -> "WireMockContainer":
        super().with_env(key, value)
        return self

    def with_exposed_ports(self, *ports) -> "WireMockContainer":
        super().with_exposed_ports(*ports)
        return self

    def with_cli_arg(self, arg_name: str, arg_value: str) -> "WireMockContainer":
        self.wire_mock_args.append(arg_name)
        self.wire_mock_args.append(arg_value)
        return self

    def with_mapping(self, name: str, data: dict[str, Any]) -> "WireMockContainer":
        self.mapping_stubs[name] = json.dumps(data)
        return self

    def with_file(self, name: str, data: dict[str, Any]):
        self.mapping_files[name] = json.dumps(data)
        return self

    def with_extension(self, class_name: str, jar_path: Path) -> "WireMockContainer":

        with open(jar_path, "rb") as fp:
            self.extensions[class_name] = fp.read()

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

    def copy_extensions_to_container(self) -> None:
        """Copies all extension jar files generated with :meth:`.with_extension`
        to the container under the configured EXTENSIONS_DIR

        ..code-block::
            wm.with_extension(
                "com.ninecookies.wiremock.extensions.JsonBodyTransformer",
                Path("extensions/wiremock-body-transformer-1.1.3.jar"
            )
        """
        self.exec("mkdir -p /var/wiremock/extensions")
        self.copy_files_to_container(
            configs=self.extensions,
            container_dir_path=Path(f"{self.EXTENSIONS_DIR}"),
            mode="wb+",
        )

    @wait_container_is_ready()
    def configure(self) -> None:
        res = urllib.request.urlopen(self.get_url("__admin/mappings"))
        if res.status != 200:
            raise Exception()

        self.copy_mappings_to_container()
        self.copy_mapping_files_to_container()
        self.copy_extensions_to_container()

        requests.post(self.get_url("__admin/mappings/reset"))

    def get_base_url(self) -> str:
        return (
            f"http://{self.get_container_host_ip()}:{self.get_exposed_port(self.port)}"
        )

    def get_url(self, path: str) -> str:
        return urljoin(self.get_base_url(), path)

    def start(self) -> "WireMockContainer":
        # TODO this causes the container to hang
        # if self.extensions.keys():
        #     self.with_cli_arg("--extensions", ",".join(self.extensions.keys()))
        cmd = " ".join(self.wire_mock_args)
        self.with_command(cmd)
        super().start()
        self.configure()
        return self


@dataclass
class WireMockServer:
    port: str
    url: str


@contextmanager
def start_wiremock_container(mapping=None, port=None):
    """
    Start a wiremock test container using Testcontainers and set up mappings.

    :param mapping: Optional dict of wiremock mappings to set up.
    :param port: Optional port to use for the wiremock container. Defaults to 8080.
    :return: URL of the running wiremock container.
    """

    client = docker.from_env()
    try:
        with WireMockContainer() as wm:
            yield wm
    except ContainerStartException as e:
        raise Exception("Error starting wiremock container") from e
    except requests.exceptions.RequestException as e:
        raise Exception("Error connecting to wiremock container") from e
    finally:
        client.close()


def wiremock_container(mapping=None, port=None):
    """
    Decorator that starts a wiremock test container using Testcontainers and sets up mappings.

    :param mapping: Optional dict of wiremock mappings to set up.
    :param port: Optional port to use for the wiremock container. Defaults to 8080.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            with start_wiremock_container(mapping=mapping, port=port) as wm:
                server = WireMockServer(port=str(wm.port), url=wm.get_url())
                return fn(server, *args, **kwargs)

        return wrapper

    return decorator
