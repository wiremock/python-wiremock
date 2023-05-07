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

client = TestClient(app)


def get_products():

    return [
        {"name": "WireMock Basic", "sku": "wm1", "price": "0.00"},
        {"name": "WireMock Pro", "sku": "wm2", "price": "500.00"},
        {"name": "WireMock Enterprise", "sku": "wm3", "price": "5000.00"},
    ]


@pytest.fixture(scope="session")
def wm():

    with WireMockServer() as wm:
        Config.base_url = f"http://localhost:{wm.port}/__admin"
        os.environ["PRODUCTS_SERVICE_HOST"] = "http://localhost"
        os.environ["PRODUCTS_SERVICE_PORT"] = str(wm.port)
        Mappings.create_mapping(
            mapping=Mapping(
                priority=100,
                request=MappingRequest(method=HttpMethods.GET, url="/products"),
                response=MappingResponse(status=200, json_body=get_products()),
                persistent=False,
            )
        )
        Mappings.create_mapping(
            mapping=Mapping(
                priority=100,
                request=MappingRequest(
                    method=HttpMethods.GET,
                    url="/products",
                    query_parameters={"product_name": {"equalTo": "WireMock Basic"}},
                ),
                response=MappingResponse(
                    status=200,
                    json_body=list(
                        filter(lambda p: p["name"] == "WireMock Basic", get_products())
                    ),
                ),
                persistent=False,
            )
        )

        yield wm


def test_get_overview_default(wm):

    resp = client.get("/overview")

    assert resp.status_code == 200
    assert resp.json() == {"products": get_products()}


def test_get_overview_with_filters(wm):

    resp = client.get("/overview?product_name=Basic")

    assert resp.status_code == 200
    assert resp.json() == {
        "products": list(
            filter(lambda p: p["name"] == "WireMock Basic", get_products())
        )
    }
