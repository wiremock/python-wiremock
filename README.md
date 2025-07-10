# Python WireMock

<p align="center">
    <a href="https://wiremock.org/docs/solutions/python/" target="_blank">
        <img width="512px" src="docs/images/python-wiremock-horizontal.png" alt="WireMock Logo"/>
    </a>
</p>

---

<table>
<tr>
<td>
<img src="https://wiremock.org/images/wiremock-cloud/wiremock_cloud_logo.png" alt="WireMock Cloud Logo" height="20" align="left">
<strong>WireMock open source is supported by <a href="https://www.wiremock.io/cloud-overview?utm_source=github.com&utm_campaign=python-wiremock-README.md-banner">WireMock Cloud</a>. Please consider trying it out if your team needs advanced capabilities such as OpenAPI, dynamic state, data sources and more.</strong>
</td>
</tr>
</table>

---

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
- Support for most of major [WireMock features ](https://wiremock.org/docs) (more on their way soon)

## References

- [Quickstart Guide](./docs/quickstart.md)
- [Installation](./docs/install.md)
- [Full documentation](http://wiremock.readthedocs.org/)

## Examples

There are several [example projects](./examples/) included to demonstrate the different ways that WireMock can be used to mock
services in your tests and systems. The example test modules demonstrate different strategies for testing against
the same "product service" and act as a good demonstration of real world applications to help you get started.

- [Testcontainers Python](examples/intro/tests/test_testcontainers.py)
- [Standalone Java Server Version](examples/intro/tests/test_java_server.py)

## Contributing

See the [Contributor Guide](./docs/CONTRIBUTING.md)
