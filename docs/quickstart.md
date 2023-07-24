# Quickstart

The preferred way of using WireMock to mock your services is by using the provided `WireMockContainer`
that uses [testcontainers-python](https://github.com/testcontainers/testcontainers-python)
and provisions WireMock as a test container on-demand.

In this example we will use the [pytest](https://docs.pytest.org/) framework.

## Prerequisites

- Python WireMock 2.6.0 or above
- Python 3.7 or above
- Pip 20.0.0 or above
- Pytest 7.3.0 or above

## Install Python WireMock

To install the most recent version of the Python WireMock library,
use the following command:

```bash
pip install wiremock
```

## Create Test Fixture

As a first step, we will need to provision a test WireMock server to be used in tests:

1. Create a pytest fixture to manage the container life-cycle.
   Use fixture `scope` to control how often the container is created
2. Set the WireMock SDK config URL to the URL exposed by the container.
   It will route all Admin API requests to
   the mock server.
3. Create REST API stub mapping for the `/hello` endpoint using the Admin SDK.

```python
import pytest

from wiremock.testing.testcontainer import wiremock_container

@pytest.fixture(scope="session") # (1)
def wm_server():
    with wiremock_container(secure=False) as wm:

        Config.base_url = wm.get_url("__admin") # (2)

        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/hello"),
                response=MappingResponse(status=200, body="hello"),
                persistent=False,
            )
        ) # (3)
        yield wm
```

## Write your first test with WireMock

Use the `wm_server` fixture in your tests and make requests against the mock server:

```python
def test_get_hello_world(wm_server):

    resp1 = requests.get(wm_server.get_url("/hello"), verify=False)

    assert resp1.status_code == 200
    assert resp1.content == b"hello"
```

## Read More

You can read more about Testcontainers support in Python WireMock [here](./testcontainers.md).

## More examples

See [this page](..) for more example references
