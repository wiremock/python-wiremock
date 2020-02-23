.PHONY: clean-pyc ext-test test upload-docs docs coverage

all: clean black test coverage

black:
	black -v -l 150 --include wiremock/*.py
	black -v -l 150 --include wiremock/base/*.py
	black -v -l 150 --include wiremock/exceptions/*.py
	black -v -l 150 --include wiremock/resources/*.py
	black -v -l 150 --include wiremock/resources/mappings/*.py
	black -v -l 150 --include wiremock/resources/near_misses/*.py
	black -v -l 150 --include wiremock/resources/requests/*.py
	black -v -l 150 --include wiremock/resources/scenarios/*.py
	black -v -l 150 --include wiremock/resources/settings/*.py
	black -v -l 150 --include wiremock/server/*.py
	black -v -l 150 --include wiremock/tests/*.py
	black -v -l 150 --include wiremock/tests/base_tests/*.py
	black -v -l 150 --include wiremock/tests/resource_tests/*.py
	black -v -l 150 --include wiremock/tests/resource_tests/mappings_tests/*.py
	black -v -l 150 --include wiremock/tests/resource_tests/near_misses_tests/*.py
	black -v -l 150 --include wiremock/tests/resource_tests/requests_tests/*.py
	black -v -l 150 --include wiremock/tests/resource_tests/scenarios_tests/*.py
	black -v -l 150 --include wiremock/tests/resource_tests/settings_tests/*.py
	black -v -l 150 --include wiremock/tests/server_tests/*.py

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
