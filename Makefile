.PHONY: clean-pyc ext-test test upload-docs docs coverage

all: clean test coverage

test:
	bash run_tests.sh

coverage:
	bash run_coverage.sh

release:
	bash deploy_to_pypi.sh

tox-test:
	PYTHONDONTWRITEBYTECODE= tox

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '#*' -exec rm -f {} +
	find . -name '.#*' -exec rm -f {} +
	find . -name '.bak' -exec rm -f {} +

docs:
	sphinx-build docs html
