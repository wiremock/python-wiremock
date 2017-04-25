# -*- coding: utf-8 -*-
"""WireMock Server Management."""
import socket

from pkg_resources import resource_filename


class WireMockServer(object):

    DEFAULT_JAVA = 'java'  # Assume java in PATH

    DEFAULT_JAR = resource_filename(
        'wiremock',
        'server/wiremock-standalone-2.6.0.jar'
    )

    def __init__(self, java_path=DEFAULT_JAVA, jar_path=DEFAULT_JAR):
        self.java_path = java_path
        self.jar_path = jar_path
        self.port = self._get_free_port()
        self.__running = False

    @property
    def is_running(self):
        return self.__running

    def _get_free_port(self):
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port