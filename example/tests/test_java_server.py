import os

import pytest
from fastapi.testclient import TestClient
from wiremock.client import (HttpMethods, Mapping, MappingRequest,
                             MappingResponse, Mappings)
from wiremock.constants import Config
from wiremock.server import WireMockServer

from product_mock.overview_service import app

client = TestClient(app)


def get_products():
    return [
        {"name": "Mock Product A", "price": 10.99, "category": "Books"},
        {"name": "Mock Product B", "price": 5.99, "category": "Movies"},
        {"name": "Mock Product C", "price": 7.99, "category": "Electronics"},
        {"name": "Mock Product D", "price": 12.99, "category": "Books"},
        {"name": "Mock Product E", "price": 8.99, "category": "Movies"},
        {"name": "Mock Product F", "price": 15.99, "category": "Electronics"},
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
                    url=r"/products?category=Books",
                    query_parameters={"category": {"equalTo": "Books"}},
                ),
                response=MappingResponse(
                    status=200,
                    json_body=list(
                        filter(lambda p: p["category"] == "Books", get_products())
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
    resp = client.get("/overview?category=Books")

    assert resp.status_code == 200
    assert resp.json() == {
        "products": list(filter(lambda p: p["category"] == "Books", get_products()))
    }
