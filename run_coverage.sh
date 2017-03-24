#!/bin/bash

mkdir ./coverage &>/dev/null
nosetests -w wiremock/tests --attr=unit --with-coverage --cover-erase --cover-package=wiremock --cover-html --cover-xml --cover-min-percentage=85 --cover-html-dir=./coverage/ --cover-xml-file=./coverage/coverage.xml
