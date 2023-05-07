# Python Wiremock Example

## Introduction

This example code demonstrates usage of python wiremock. The example code demonstrates a fictional set of microservices
where the `overview_service` depends on the display of products returned from the `products_service`.

When the services are run normally the Overview service makes a request to the Products services and the list of
products returned by the Product Service is displayed to the user.

```
+-----------------+               +-----------------+
| Overview Service|               | Products Service|
+-----------------+               +-----------------+
        |                                  |
        |         GET /products            |
        |--------------------------------->|
        |                                  |
        |       List of products           |
        |<---------------------------------|
        |                                  |
        |     Display products to user     |
        |--------------------------------->|
        |                                  |
```

When we are writing tests to ensure that the Overview Service works correctly, we do not want to have the overview service
have to depend on real requests being made to the products services. This normally leads to the code being mocked, and other approaches that
are hard to maintain and dont allow us to test the code closer to real world conditions.

Ultimately, we want a real http request to happen under test conditions so that the tests and the code operate as if the products
services is running and returning actual http responses. In tests we also need to be able to control what this system returns
so that we can assert the code acts in certain ways when it gets certain responses from the server.

This is what python-wiremock helps to solve.

The example code demonstrates how to use python-wiremock to run a test server directly from our tests that give us
full control over how the mock service should handle our requests. We can generate respones directly from the tests
to allow us to write solid integration tests that dont involved mockig the code we're trying to test.

## Running the tests

To run the tests use docker-compose to create the necessary containers.

`docker-compose run overview_srv pytest --tb=short`

## How we use this example code base

As well as serving as a working example of how to work with python wiremock, this example code base is also used as a "e2e" test suite of sorts.
The docker-compose configuration bundles the python-wiremock code directly into the container so that we can actually iterate on changes against a
real world example.
