CODE_DIRS := ./application
PYPROJECT_TOML := pyproject.toml
TEST_COV_FAILURE_PC := 80

.PHONY: help
help:				## Show the help.
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: import-check
import-check:			## Check for Python import errors
	@echo Checking for Python Import Errors...
	poetry run isort $(CODE_DIRS) --settings-file $(PYPROJECT_TOML) --check-only --color
	@echo Python Import Checking Complete

.PHONY: formatting-check
formatting-check:		## Check for Python formatting errors
	@echo Checking for Python Formatting Errors...
	poetry run black $(CODE_DIRS) --config $(PYPROJECT_TOML) --check --color
	@echo Python Format Checking Complete

.PHONY: pylint
pylint:				## Check for Python linting errors (Pylint)
	@echo Checking for Python Pylint Errors...
	poetry run pylint $(CODE_DIRS) --rcfile .pylintrc --fail-under 9.0 --fail-on=E --output-format colorized --disable fixme
	@echo Python Pylint Checking Complete

.PHONY: type-check
type-check:			## Check for Python type hinting errors
	@echo Checking for Python Type Hinting Errors...
	poetry run mypy $(CODE_DIRS) --config-file $(PYPROJECT_TOML)
	@echo Python Type Checking Complete

.PHONY: backend-install
backend-install:		## Install the project in dev mode.
	rm -rf .venv
	python3.13 -m poetry install

.PHONY: backend-show
backend-show:			## Show the current environment.
	@echo "Current environment:"
	@poetry env info

.PHONY: backend-lint
backend-lint: 			import-check formatting-check pylint type-check ## Apply all linting operations