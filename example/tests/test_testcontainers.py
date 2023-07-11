import os

import pytest
from fastapi.testclient import TestClient
from wiremock.client import Mappings
from wiremock.constants import Config
from wiremock.testing.testcontainer import wiremock_container

from product_mock.overview_service import app

from .utils import get_mappings, get_products

client = TestClient(app)


@pytest.fixture(scope="module")
def wm_docker():
    with wiremock_container(verify_ssl_certs=False, secure=False) as wm:

        Config.base_url = wm.get_url("__admin")

        os.environ["PRODUCTS_SERVICE_HOST"] = wm.get_base_url()

        [Mappings.create_mapping(mapping=mapping) for mapping in get_mappings()]

        yield wm

        Mappings.delete_all_mappings()


@pytest.mark.usefixtures("wm_docker")
def test_get_overview_default():
    resp = client.get("/overview")

    assert resp.status_code == 200
    assert resp.json() == {"products": get_products()}


@pytest.mark.usefixtures("wm_docker")
def test_get_overview_with_filters():
    resp = client.get("/overview?category=Books")

    assert resp.status_code == 200
    assert resp.json() == {
        "products": list(filter(lambda p: p["category"] == "Books", get_products()))
    }
