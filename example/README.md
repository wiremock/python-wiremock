## Python Wiremock Example

This example code demonstrates usage of python wiremock. The example code demonstrates a simple set of microservices
where the overview_services depends on display products normally returned from the products_service.

when the services are run normally the Overview service makes a request to the Products services and the list of
products returned by the Product Service is displayed to the user.

When we are writing tests to ensure that the Overview Service works correctly, we do not want to have the overview service
have to depend on real requests being made to the products services. This normally needs to mocks and other approaches that
are hard to maintain and dont allow us to test the code closer to real world conditions.

Ultimately, we want a real http request to happen under test conditions so that the tests and the code operate a if the products
services is really running and returning actual http responses. In tests we also need to be able to control what this system returns
so that we can assert the code acts in certain ways when it gets certain responses from the server.

This is what python-wiremock helps to solve.

The example code demonstrates how to use python-wiremock to run a test server directly from our tests that give us
full control over how the mock service should handle our requests. We can generate respones directly from the tests
to allow us to write solid integration tests that dont involved mockig the code we're trying to test.

- We need to install the dependencies of wiremock in the package as the wiremock module
  is installed without the dependencies
