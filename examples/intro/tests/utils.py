from wiremock.client import HttpMethods, Mapping, MappingRequest, MappingResponse


def get_products():
    return [
        {"name": "Mock Product A", "price": 10.99, "category": "Books"},
        {"name": "Mock Product B", "price": 5.99, "category": "Movies"},
        {"name": "Mock Product C", "price": 7.99, "category": "Electronics"},
        {"name": "Mock Product D", "price": 12.99, "category": "Books"},
        {"name": "Mock Product E", "price": 8.99, "category": "Movies"},
        {"name": "Mock Product F", "price": 15.99, "category": "Electronics"},
    ]


def get_mappings() -> list[Mapping]:
    return [
        Mapping(
            priority=100,
            request=MappingRequest(method=HttpMethods.GET, url="/products"),
            response=MappingResponse(status=200, json_body=get_products()),
            persistent=False,
        ),
        Mapping(
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
        ),
    ]
