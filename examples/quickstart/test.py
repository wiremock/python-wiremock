import pytest

from wiremock.testing.testcontainer import wiremock_container

@pytest.fixture(scope="session") # (1)
def wm_server():
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


def test_get_hello_world(wm_server): # (4)

    resp1 = requests.get(wm_server.get_url("/hello"), verify=False)

    assert resp1.status_code == 200
    assert resp1.content == b"hello"
