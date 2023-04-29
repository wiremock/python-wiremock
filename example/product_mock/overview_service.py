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
        "PRODUCTS_SERVICE_HOST", "http://products_srv"
    )
    PRODUCTS_SERVICE_PORT = os.environ.get("PRODUCTS_SERVICE_PORT", 5002)

    PRODUCTS_URL = f"{PRODUCTS_SERVICE_HOST}:{PRODUCTS_SERVICE_PORT}/products"

    products = requests.get(PRODUCTS_URL)
    return {"products": products.json()}
