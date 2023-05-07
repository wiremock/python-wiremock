import os

import pytest
from fastapi.testclient import TestClient
from wiremock.client import Mappings
from wiremock.constants import Config
from wiremock.testing.testcontainer import WireMockServer, start_wiremock_container

from product_mock.overview_service import app

from .utils import get_mappings, get_products

client = TestClient(app)


@pytest.fixture(scope="module")
def wm_docker():
    with start_wiremock_container() as wm:
        server = WireMockServer(port=str(wm.port), url=wm.get_url())
        Config.base_url = f"{wm.get_url()}/__admin"
        os.environ["PRODUCTS_SERVICE_HOST"] = f"http://{wm.get_container_host_ip()}"
        os.environ["PRODUCTS_SERVICE_PORT"] = str(wm.port)
        [Mappings.create_mapping(mapping=mapping) for mapping in get_mappings()]

        yield server

        Mappings.delete_all_mappings()


def test_get_overview_default(wm_docker):
    resp = client.get("/overview")

    assert resp.status_code == 200
    assert resp.json() == {"products": get_products()}


def test_get_overview_with_filters(wm_docker):
    resp = client.get("/overview?category=Books")

    assert resp.status_code == 200
    assert resp.json() == {
        "products": list(filter(lambda p: p["category"] == "Books", get_products()))
    }
