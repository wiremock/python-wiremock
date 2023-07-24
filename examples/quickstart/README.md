# Python WireMock - Quickstart

This example shows using WireMock to mock your services is by using the provided `WireMockContainer`
that uses [testcontainers-python](https://github.com/testcontainers/testcontainers-python)
and provisions WireMock as a test container on-demand.

See the step-by-step guide [here](../../docs/quickstart.md)

## Prerequisites

- Python 3.7 or above
- Pip 20.0.0 or above (use `apt install python3-pip`, for example)
- Pytest 7.3.0 or above (use `pip install pytest`)
- Testcontainers 3.5.0 or above (use `pip install testcontainers`)

## TL;DR

```bash
pip install wiremock
pytest test.py -v 
```
