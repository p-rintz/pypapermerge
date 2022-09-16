#
# Settings
#

.ONESHELL:
TESTS_DIR ?= tests
DOCKER_RUN = docker compose -f $(TESTS_DIR)/docker-compose.yaml --env-file $(TESTS_DIR)/docker-env up -d
PROJECT = pypapermerge


#
# Targets
#

venv: venv/touchfile

venv/touchfile: requirements.txt requirements_dev.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate; pip install -Ur requirements.txt -Ur requirements_dev.txt
	touch venv/touchfile

setup: venv
	$(DOCKER_RUN)

docs: venv
	mkdocs build

install: venv
	pip3 install .

tests: setup
	python -m pytest --cov-report term-missing --cov=$(PROJECT) $(TESTS_DIR)

coverage-report: setup
	python -m pytest --cov-report xml --cov=$(PROJECT) $(TESTS_DIR)

lint: venv
	isort .
	black .
	pylint $(PROJECT)

lint-check: venv
	isort . --check-only --diff --color
	black . --check --diff --color
	pylint $(PROJECT)

docs-deploy: venv
	mkdocs gh-deploy

release: coverage-report lint docs-deploy
