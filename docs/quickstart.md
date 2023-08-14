# Quickstart

The preferred way of using WireMock to mock your services is by using the provided `WireMockContainer`
that uses [testcontainers-python](https://github.com/testcontainers/testcontainers-python)
and provisions WireMock as a test container on-demand.

In this example we will use the [pytest](https://docs.pytest.org/) framework.

## Prerequisites

- Python 3.7 or above
- Pip 20.0.0 or above (use `apt install python3-pip`, for example)
- Pytest 7.3.0 or above (use `pip install pytest`)
- Testcontainers 3.5.0 or above (use `pip install testcontainers`)

## Install Python WireMock

To install the most recent version of the Python WireMock library,
use the following command:

```bash
pip install wiremock
```

## Create the Test Fixture

As a first step, we will need to provision a test WireMock server to be used in tests:

1. Create an empty `test.py` file
2. In this file, create a pytest fixture to manage the container life-cycle.
   Use fixture `scope` to control how often the container is created
3. Set the WireMock SDK config URL to the URL exposed by the container.
   It will route all Admin API requests to
   the mock server.
4. Create REST API stub mapping for the `/hello` endpoint using the Admin SDK.

```python
import pytest
import requests

from wiremock.testing.testcontainer import wiremock_container
from wiremock.constants import Config
from wiremock.client import *

@pytest.fixture # (1)
def wiremock_server():
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

Use the `wiremock_server` fixture in your tests and make requests against the mock server.
Add the following test to the `test.py` file:

```python
def test_get_hello_world(wiremock_server): # (4)
    response = requests.get(wiremock_server.get_url("/hello"))

    assert response.status_code == 200
    assert response.content == b"hello"
```

## Run the test!

Run the following command:

```bash
pytest test.py -v
```

Sample output:

```
$ pytest test.py -v
================ test session starts ================
platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /c/Users/Oleg/Documents/opensource/wiremock/python-wiremock
configfile: pyproject.toml
plugins: anyio-3.7.1
collected 1 item

test.py::test_get_hello_world PASSED                                [100%]
```

## Read More

You can read more about Testcontainers support in Python WireMock [here](./testcontainers.md).

## More examples

See [this page](./examples.md) for more example references
