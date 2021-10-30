from calendar import timegm
from copy import deepcopy
import logging
from typing import Dict, Any, Union
import datetime

from wiremock import __version__


logger = logging.getLogger("wiremock")


DEFAULT_TIMEOUT: int = 30
DEFAULT_BASE_URL: str = "http://localhost/__admin"
USER_AGENT: str = "python_wiremock/%s".format(__version__)
DEFAULT_HEADERS: Dict[str, Any] = {"Accept": "application/json", "Content-Type": "application/json", "user-agent": USER_AGENT}
DEFAULT_REQUESTS_VERIFY: bool = True
DEFAULT_REQUESTS_CERT: Union[None, str] = None


class Config(object):
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    timeout: int = DEFAULT_TIMEOUT
    base_url: str = DEFAULT_BASE_URL
    user_agent: str = USER_AGENT
    headers: Dict[str, Any] = DEFAULT_HEADERS
    requests_verify: bool = DEFAULT_REQUESTS_VERIFY
    requests_cert: Union[None, str] = DEFAULT_REQUESTS_CERT


Config.instance()  # pre-call once


def make_headers(**kwargs) -> Dict[str, Any]:
    headers = deepcopy(Config.instance().headers)
    for key, value in kwargs.items():
        headers[key] = value
    return headers


def datetime_to_ms(dt: Union[int, datetime.datetime]) -> int:
    if isinstance(dt, int):
        return dt
    else:
        tmp = timegm(dt.utctimetuple())
        tmp += float(dt.microsecond) / 1000000.0
        return int(tmp * 1000.0)


__all__ = ["Config", "make_headers", "logger", "datetime_to_ms"]
