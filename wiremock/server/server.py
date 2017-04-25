# -*- coding: utf-8 -*-
"""WireMock Server Management."""
import atexit
import socket

from pkg_resources import resource_filename
from subprocess import Popen, PIPE, STDOUT

from wiremock.server.exceptions import (
    WireMockServerAlreadyStartedError,
    WireMockServerNotStartedError
)


class WireMockServer(object):

    DEFAULT_JAVA = 'java'  # Assume java in PATH
    DEFAULT_JAR = resource_filename('wiremock', 'server/wiremock-standalone-2.6.0.jar')

    def __init__(self, java_path=DEFAULT_JAVA, jar_path=DEFAULT_JAR):
        self.java_path = java_path
        self.jar_path = jar_path
        self.port = self._get_free_port()
        self.__subprocess = None
        self.__running = False

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
            raise WireMockServerAlreadyStartedError(
                'WireMockServer already started on port {}'.format(self.port)
            )

        cmd = [self.java_path, '-jar', self.jar_path, '--port', str(self.port)]
        atexit.register(self.stop)
        self.__subprocess = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.__running = True

    def stop(self):
        try:
            self.__subprocess.kill()
        except AttributeError:
            raise WireMockServerNotStartedError()

    def _get_free_port(self):
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port