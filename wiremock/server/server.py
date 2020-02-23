# -*- coding: utf-8 -*-
"""WireMock Server Management."""
import atexit
import socket

import time

import requests
from pkg_resources import resource_filename
from subprocess import Popen, PIPE, STDOUT

from wiremock.server.exceptions import WireMockServerAlreadyStartedError, WireMockServerNotStartedError


class WireMockServer(object):

    DEFAULT_JAVA = "java"  # Assume java in PATH
    DEFAULT_JAR = resource_filename("wiremock", "server/wiremock-standalone-2.6.0.jar")

    def __init__(self, java_path=DEFAULT_JAVA, jar_path=DEFAULT_JAR, port=None, max_attempts=10):
        self.java_path = java_path
        self.jar_path = jar_path
        self.port = port or self._get_free_port()
        self.__subprocess = None
        self.__running = False
        self.max_attempts = max_attempts

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    @property
    def is_running(self):
        return self.__running

    def start(self):
        if self.is_running:
            raise WireMockServerAlreadyStartedError("WireMockServer already started on port {}".format(self.port))

        cmd = [self.java_path, "-jar", self.jar_path, "--port", str(self.port)]
        try:
            self.__subprocess = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        except OSError as e:
            raise WireMockServerNotStartedError(str(e))  # Problem with Java

        time.sleep(0.1)
        if self.__subprocess.poll() is not None:
            # Process complete - server not started
            raise WireMockServerNotStartedError(
                "\n".join(["returncode: {}".format(self.__subprocess.returncode), "stdout:", str(self.__subprocess.stdout.read())])
            )

        # Call the /__admin endpoint as a check for running state
        attempts = 0
        success = False
        while attempts < self.max_attempts:
            attempts += 1
            resp = requests.get("http://localhost:{}/__admin".format(self.port))
            if resp.status_code == 200:
                success = True
                break
            time.sleep(0.25)

        if not success:
            raise WireMockServerNotStartedError("unable to get a successful GET http://localhost:{}/__admin response".format(self.port))

        atexit.register(self.stop, raise_on_error=False)
        self.__running = True

    def stop(self, raise_on_error=True):
        try:
            self.__subprocess.kill()
        except AttributeError:
            if raise_on_error:
                raise WireMockServerNotStartedError()

    def _get_free_port(self):
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        address, port = s.getsockname()
        s.close()
        return port
