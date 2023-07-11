# Python WireMock Admin API Client

<p align="center">
    <a href="https://wiremock.org/docs/solutions/python/" target="_blank">
        <img width="512px" src="docs/images/python-wiremock-horizontal.png" alt="WireMock Logo"/>
    </a>
</p>

Python Wiremock is an HTTP client that allows users to interact with a Wiremock instance from within a Python project.

[![a](https://img.shields.io/badge/slack-%23wiremock%2Fpython-brightgreen?style=flat&logo=slack)](https://slack.wiremock.org/)
[![Coverage Status](https://coveralls.io/repos/github/wiremock/python-wiremock/badge.svg?branch=master)](https://coveralls.io/github/wiremock/python-wiremock?branch=master)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://wiremock.readthedocs.org/)

## Key Features

WireMock can run in unit tests, as a standalone process or a container. Key features include:

- Supports most of the major [Wiremock](https://wiremock.org/docs) features (more on their way soon)
- Support for [testcontainers-python](https://github.com/testcontainers/testcontainers-python) to easily start wiremock server for your tests
- Support for standalone wiremock JAVA sever

## Install as Dependency

To install:

    `pip install wiremock`

To install with testing dependencies:

    `pip install wiremock[testing]`

To install via Poetry:

    `poetry add --extras=testing wiremock`

## Quick Start

The preferred way of using WireMock to mock your services is by using the provided `WireMockContainer` [testcontainers-python](https://github.com/testcontainers/testcontainers-python).

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

You can read more about Testcontainers support in python-wiremock [here](docs/testcontainers.md).

## Examples

There are several example projects included to demonstrate the different ways that wiremock can be used to mock
services in your tests and systems. The example test modules demonstrate different strategies for testing against
the same "product service" and act as a good demonstration of real world applications to help you get started.

- [Python Testcontainers](examples/tests/test_containers.py)

- [Standlone JAVA Server Version](examples/tests/test_java_server.py)

## Documentation

wiremock documentation can be found at http://wiremock.readthedocs.org/

## Pull Requests

General Rules:

- All Tests must pass
- Coverage shouldn't decrease
- All Pull Requests should be rebased against master **before** submitting the PR.

## Development

Setup the project using poetry.

`poetry install`
