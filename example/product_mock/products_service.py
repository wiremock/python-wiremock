from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/products")
async def read_products(category: str = None, sort_by: str = None):
    products = [
        {"name": "Product A", "price": 10.99, "category": "Books"},
        {"name": "Product B", "price": 5.99, "category": "Movies"},
        {"name": "Product C", "price": 7.99, "category": "Electronics"},
        {"name": "Product D", "price": 12.99, "category": "Books"},
        {"name": "Product E", "price": 8.99, "category": "Movies"},
        {"name": "Product F", "price": 15.99, "category": "Electronics"},
    ]

    if category:
        products = [p for p in products if p["category"] == category]

    if sort_by:
        products = sorted(products, key=lambda p: p[sort_by])

    return {"products": products}
