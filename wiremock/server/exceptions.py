# -*- coding: utf-8 -*-
"""WireMockServer Exceptions."""


class WireMockServerException(Exception):
    pass


class WireMockServerAlreadyStartedError(WireMockServerException):
    pass


class WireMockServerNotStartedError(WireMockServerException):
    pass
