#!/bin/bash
#
# Deploy to PyPI for both source and wheel
#
rm -Rf build/ dist/ wiremock.egg-info/ || true
python setup.py sdist upload -r local || true
export WHEEL_TOOL=`which wheel` && python setup.py bdist_wheel --universal upload -r local || true
rm -Rf build/ dist/ wiremock.egg-info/ || true
