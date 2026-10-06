#!/bin/sh

rm -Rf build/ dist/ wiremock.egg-info coverage/ wiremock/tests/coverage/ html/ || true
# Container tests need a Docker daemon.
if docker info >/dev/null 2>&1; then
    set --
else
    echo "Docker not available, skipping tests/test_containers.py"
    set -- --ignore=tests/test_containers.py
fi
uv run pytest tests/ --cov=wiremock --tb=short "$@"
