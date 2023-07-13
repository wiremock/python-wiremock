import os

import pytest
from fastapi.testclient import TestClient
from wiremock.client import Mappings
from wiremock.constants import Config
from wiremock.server import WireMockServer

from product_mock.overview_service import app

from .utils import get_mappings, get_products

client = TestClient(app)


@pytest.fixture(scope="module")
def wm_java():
    with WireMockServer() as _wm:
        Config.base_url = f"http://localhost:{_wm.port}/__admin"
        os.environ["PRODUCTS_SERVICE_HOST"] = f"http://localhost:{_wm.port}"
        [Mappings.create_mapping(mapping=mapping) for mapping in get_mappings()]

        yield _wm

        Mappings.delete_all_mappings()


def test_get_overview_default(wm_java):
    resp = client.get("/overview")

    assert resp.status_code == 200
    assert resp.json() == {"products": get_products()}


def test_get_overview_with_filters(wm_java):
    resp = client.get("/overview?category=Books")

    assert resp.status_code == 200
    assert resp.json() == {
        "products": list(filter(lambda p: p["category"] == "Books", get_products()))
    }
