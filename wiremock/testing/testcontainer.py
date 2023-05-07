import os
import socket
import urllib
from contextlib import contextmanager
from dataclasses import dataclass

import docker
import requests
from testcontainers.core.container import DockerContainer
from testcontainers.core.exceptions import ContainerStartException
from testcontainers.core.waiting_utils import (wait_container_is_ready,
                                               wait_for_logs)


class WireMockContainer(DockerContainer):
    """
    Wiremock container.
    """

    def __init__(
        self, image: str = "wiremock/wiremock", port: int = 8080, **kwargs
    ) -> None:
        self.port = port
        super(WireMockContainer, self).__init__(image, **kwargs)
        self.with_bind_ports(8080, 8080)
        self.with_volume_mapping("/var/run/docker.sock", "/var/run/docker.sock")
        self.with_env("JAVA_OPTS", "-Djava.net.preferIPv4Stack=true")

    @wait_container_is_ready()
    def _connect(self) -> None:
        res = urllib.request.urlopen(f"{self.get_url()}/__admin/mappings")
        if res.status != 200:
            raise Exception()

    def get_url(self) -> str:
        host = self.get_container_host_ip()
        port = self.get_exposed_port(self.port)
        return f"http://{host}:{port}"

    def start(self) -> "WireMockContainer":
        super().start()
        self._connect()
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
