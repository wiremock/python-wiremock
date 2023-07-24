import os

import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/overview")
async def read_products(category: str = "", sort_by: str = ""):
    PRODUCTS_SERVICE_HOST = os.environ.get(
        "PRODUCTS_SERVICE_HOST", "http://products_srv:5002"
    )

    PRODUCTS_URL = f"{PRODUCTS_SERVICE_HOST}/products"

    params = {}
    if category != "":
        params["category"] = category
    if sort_by != "":
        params["sort_by"] = sort_by

    products_resp = requests.get(PRODUCTS_URL, params=params)
    if products_resp.status_code < 300:
        return {"products": products_resp.json()}
    else:
        return {
            "error": True,
            "error_message": products_resp.content,
            "error_status": products_resp.status_code,
        }
