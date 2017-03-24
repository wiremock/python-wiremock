#!/bin/bash

sphinx-build docs html
watchmedo shell-command -R --command 'sphinx-build docs html' ./docs/
