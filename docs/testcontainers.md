# Python WireMock Test Containers

Python wiremock ships with support for [python-testcontainers](https://github.com/testcontainers/testcontainers-python) to eaily start wiremock server from your test suite using python.

## Using the context manager

The simplest way to integrate the wirmock container into your test suite is to use the `wiremock_container` context manager. For pytest users this can be
used in conjuction with a pytest fixture to easily manage the life-cycle of the container.

```python
import pytest

from wiremock.testing.testcontainer import wiremock_container

# Create a pytest fixture to manage the container life-cycle
@pytest.fixture(scope="session")
def wm_server():
    with wiremock_container(secure=False) as wm:

        # set the wiremock sdk config url to the url exposed by the container
        Config.base_url = wm.get_url("__admin")

        # Generate mappings using the sdk
        Mappings.create_mapping(
            Mapping(
                request=MappingRequest(method=HttpMethods.GET, url="/hello"),
                response=MappingResponse(status=200, body="hello"),
                persistent=False,
            )
        )
        yield wm


def test_get_hello_world(wm_server):

    resp1 = requests.get(wm_server.get_url("/hello"), verify=False)

    assert resp1.status_code == 200
    assert resp1.content == b"hello"
```

The context manager will automatically start the container. This is typically what you want as any attempts to generate urls to the contianer when it's not running will result in errors.

If you do need to start the container manually yourself, you can pass `start=False` to the context manager and the context manager will simply yield the instance of the container without starting it.

The `wiremock_container` also supports generating mapping request and response files for you via the mappings kwarg.

```python

@pytest.mark.container_test
def test_configure_via_wiremock_container_context_manager():

    mappings = [
        (
            "hello-world.json",
            {
                "request": {"method": "GET", "url": "/hello"},
                "response": {"status": 200, "body": "hello"},
            },
        )
    ]

    with wiremock_container(mappings=mappings, verify_ssl_certs=False) as wm:

        resp1 = requests.get(wm.get_url("/hello"), verify=False)
        assert resp1.status_code == 200
        assert resp1.content == b"hello"
```

The `wiremock_container` context manager offers a number of other useful options to help to configure the container. See the `wirewmock.testing.testcontainer.wiremock_container` method for the full description
of options.

## Using the WireMockContainer directly

You can also instantiate the container instance yourself using `WireMockContainer`. The container itself provides methods for creating mapping files and stubs on the container instance which can be used as an alternative
if you maintainf your request and response stubs as files.

```python
WireMockContainer(verify_ssl_certs=False)
    .with_mapping(
        "hello-world.json",
        {
            "request": {"method": "GET", "url": "/hello"},
            "response": {"status": 200, "body": "hello"},
        },
    )
    .with_mapping(
        "hello-world-file.json",
        {
            "request": {"method": "GET", "url": "/hello2"},
            "response": {"status": 200, "bodyFileName": "hello.json"},
        },
    )
    .with_file("hello.json", {"message": "Hello World !"})
    .with_cli_arg("--verbose", "")
    .with_cli_arg("--root-dir", "/home/wiremock")
    .with_env("JAVA_OPTS", "-Djava.net.preferIPv4Stack=true")
)
```
