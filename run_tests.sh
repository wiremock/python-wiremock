#!/bin/sh

rm -Rf build/ dist/ wiremock.egg-info coverage/ wiremock/tests/coverage/ html/ || true
echo -e 'y\n' | pip uninstall wiremock
pytest -vv -m "unit" wiremock/tests/*
