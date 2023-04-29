import os

import pytest
from fastapi.testclient import TestClient
from wiremock.client import (
    HttpMethods,
    Mapping,
    MappingRequest,
    MappingResponse,
    Mappings,
)
from wiremock.constants import Config
from wiremock.server import WireMockServer

from product_mock.overview_service import app

mapping = Mapping(
    priority=100,
    request=MappingRequest(method=HttpMethods.GET, url="/products"),
    response=MappingResponse(status=200, json_body=[]),
    persistent=False,
)


client = TestClient(app)


@pytest.fixture(scope="session")
def wm():

    with WireMockServer() as wm:
        Config.base_url = f"http://localhost:{wm.port}/__admin"
        os.environ["PRODUCTS_SERVICE_HOST"] = "http://localhost"
        os.environ["PRODUCTS_SERVICE_PORT"] = str(wm.port)
        Mappings.create_mapping(mapping=mapping)

        yield wm


def test_foo(wm):

    resp = client.get("/overview")

    assert resp.status_code == 200
    assert resp.json() == {"products": []}
