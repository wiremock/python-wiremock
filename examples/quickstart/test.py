import pytest
import requests

from wiremock.testing.testcontainer import wiremock_container
from wiremock.constants import Config
from wiremock.client import *

@pytest.fixture # (1)
def wiremock_server():
    with wiremock_container(secure=False) as wm:
        Config.base_url = wm.get_url("__admin") # (2)
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/hello"),
                response=MappingResponse(status=200, body="hello"),
                persistent=False,
            )
        ) # (3)      
        yield wm

def test_get_hello_world(wiremock_server): # (4)
    response = requests.get(wiremock_server.get_url("/hello"))

    assert response.status_code == 200
    assert response.content == b"hello"
