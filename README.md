# Python WireMock

<p align="center">
    <a href="https://wiremock.org/docs/solutions/python/" target="_blank">
        <img width="512px" src="docs/images/python-wiremock-horizontal.png" alt="WireMock Logo"/>
    </a>
</p>

Python WireMock is a library that allows users to interact with a WireMock instance from within a Python project.
Full documentation can be found at [wiremock.readthedocs.org](http://wiremock.readthedocs.org/).

[![a](https://img.shields.io/badge/slack-%23wiremock%2Fpython-brightgreen?style=flat&logo=slack)](https://slack.wiremock.org/)
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](http://wiremock.readthedocs.org/)

<!--
FIXME: Reporting is dead: https://github.com/wiremock/python-wiremock/issues/74
[![Coverage Status](https://coveralls.io/repos/github/wiremock/python-wiremock/badge.svg?branch=master)](https://coveralls.io/github/wiremock/python-wiremock?branch=master)
-->

## Key Features

WireMock can run in unit tests, as a standalone process or a container. Key features include:

- [Testcontainers Python](https://github.com/testcontainers/testcontainers-python) module to easily start WireMock server for your tests
- REST API Client for a standalone WireMock Java server
- Supports most of the major [Wiremock](https://wiremock.org/docs) features (more on their way soon)

## References

- [Quickstart Guide](./docs/quickstart.md)
- [Installation](./docs/install.md)
- [Full documentation](http://wiremock.readthedocs.org/)

## Examples

There are several example projects included to demonstrate the different ways that wiremock can be used to mock
services in your tests and systems. The example test modules demonstrate different strategies for testing against
the same "product service" and act as a good demonstration of real world applications to help you get started.

- [Testcontainers Python](example/tests/test_testcontainers.py)
- [Standalone Java Server Version](example/tests/test_java_server.py)
