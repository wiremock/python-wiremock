#!/bin/bash
#
# Deploy to PyPI for both source and wheel
#
rm -Rf build/ dist/ wiremock.egg-info/ || true
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
rm -Rf build/ dist/ wiremock.egg-info/ || true
