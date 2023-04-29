import pytest

from wiremock.base import RestClient
from wiremock.constants import Config


@pytest.fixture
def client():
    Config.base_url = "http://localhost/__admin"
    Config.timeout = 1
    return RestClient()
