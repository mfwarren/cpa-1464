all: flakes test

test:: run_integration_tests run_acceptance_tests

unit_test:: run_unit_tests

acceptance_test:: run_acceptance_tests

analysis:: flakes

flakes:
	@echo Searching for static errors...
	@flake8 --statistics --count  src/cpa-1464 tests

coveralls::
	coveralls

publish::
	@python setup.py sdist bdist_wheel upload
	@python -m releaseme --git --file src/cpa-1464/__init__.py

run_unit_tests::
	@echo Running Tests...
	@py.test --cov cpa-1464 --cov-report=term-missing --no-cov-on-fail tests/unit

run_integration_tests::
	@echo Running Tests...
	@py.test --cov cpa-1464 --cov-report=term-missing --no-cov-on-fail tests/unit tests/integration

run_acceptance_tests::
	@echo Running Tests...
	@py.test tests/acceptance
