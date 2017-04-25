# -*- coding: utf-8 -*-
"""TODO: Document exceptions here.

Copyright (C) 2017, Auto Trader UK
Created 25. Apr 2017 14:19
Creator: john.harrison

"""


class WireMockServerException(Exception):
    pass


class WireMockServerAlreadyStartedError(WireMockServerException):
    pass


class WireMockServerNotStartedError(WireMockServerException):
    pass
