Quickstart
=====

The preferred way of using WireMock to mock your services is by using the provided `WireMockContainer`
that uses [testcontainers-python](https://github.com/testcontainers/testcontainers-python)
and provisions WireMock as a test container on-demand.

### Prerequisites

- Python 3.7 or above
- Pip 20.0.0 or above

### Install Python WireMock

```bash
pip install wiremock
```

### Use Python WireMock

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


def test_get_hello_world(wm_server): # (4)

    resp1 = requests.get(wm_server.get_url("/hello"), verify=False)

    assert resp1.status_code == 200
    assert resp1.content == b"hello"
```

1. Create a pytest fixture to manage the container life-cycle. use fixture `scope` to control how often the container is created

2. Set the wiremock sdk config url to the url exposed by the container

3. Create response and request mappings using the Admin SDK.

4. Use the `wm_server` fixture in your tests and make requests against the mock server.

You can read more about Testcontainers support in Python WireMock [here](./testcontainers.md).

## More examples

See [this page](..) for more example references
