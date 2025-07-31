#!/bin/sh

rm -Rf build/ dist/ wiremock.egg-info coverage/ wiremock/tests/coverage/ html/ || true
uv run pytest --cov=wiremock --tb=short
