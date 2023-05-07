import os

import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/overview")
async def read_products(
    product_name: str | None = None, category: str = "", sort_by: str = ""
):
    PRODUCTS_SERVICE_HOST = os.environ.get(
        "PRODUCTS_SERVICE_HOST", "http://products_srv"
    )
    PRODUCTS_SERVICE_PORT = os.environ.get("PRODUCTS_SERVICE_PORT", 5002)

    PRODUCTS_URL = f"{PRODUCTS_SERVICE_HOST}:{PRODUCTS_SERVICE_PORT}/products"

    params = {}
    if product_name is not None:
        params["product_name"] = product_name

    products_resp = requests.get(PRODUCTS_URL, params=params)
    if products_resp.status_code < 300:
        return {"products": products_resp.json()}
    else:
        return {"products": []}
