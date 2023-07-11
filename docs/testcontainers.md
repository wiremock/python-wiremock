# WireMock module for Testcontainers Python

Python WireMock ships with support for [testcontainers-wiremock](https://github.com/testcontainers/testcontainers-python) to easily start WireMock server from your test suite using Python.

## Using the context manager

The simplest way to integrate the WireMock container into your test suite is to use the `wiremock_container` context manager. For pytest users this can be
used in conjuction with a pytest fixture to easily manage the life-cycle of the container.

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
if you maintain your request and response stubs as files.

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

## Using WireMockContainer inside Docker (dind)

It's common that you might need to start Testcontainers from inside of another container. The example project in [Testcontainer Example](../example/docker-compose.yaml) actually does this.

When running spawning testcontainer inside of another container you will need to set the `WIREMOCK_DIND` config variable to true. When this env var is set the host of the wiremock container
will explicitly be set to `host.docker.internal`.

Let's take a look at the example docker-compose.yaml the example products service uses.

```yaml
version: "3"

services:
  overview_srv:
    build:
      context: ../
      dockerfile: example/Dockerfile
    ports:
      - "5001:5001"
    environment:
      - WIREMOCK_DIND=true # (1) Set the env var
    extra_hosts:
      - "host.docker.internal:host-gateway" # (2)
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock # (3)
      - ..:/app/
      - .:/app/example/
    command: uvicorn product_mock.overview_service:app --host=0.0.0.0 --port=5001
```

1. Set the environment variable to instruct WireMockContainer that we're running in `DIND` mode.

2. Map the host.docker.internal to host-gateway. Docker will magically replace the host-gateway value with the ip of the container.
   This mapping is required when using dind on certain CI system like github actions.

3. Mount the docker binary into the container
