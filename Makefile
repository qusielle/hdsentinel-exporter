SHELL := /bin/bash

.PHONY: autopep
autopep:
	autopep8 -aaaa --exit-code --in-place --max-line-length 99 --recursive --exclude .pipenv .

.PHONY: flake8
flake8:
	flake8 --max-line-length 99 --exclude .pipenv .

.PHONY: mypy
mypy:
	mypy --exclude .pipenv .

.PHONY: lint
lint: autopep flake8 mypy

.coverage:
	coverage run -m pytest -vv .

coverage.xml: .coverage
	coverage report
	coverage xml -o $@

.PHONY: test
test: .coverage

.PHONY: coverage
coverage: coverage.xml

.PHONY: docker-build
docker-build:
	docker build --network host --tag hdsentinel_exporter .

env_exporter_variables := $(shell \
	compgen -A variable HDS_EXP_ | while read var; do \
		echo "-e $${var}=$${!var}"; \
	done \
)

.PHONY: docker-run
docker-run: docker-build
	docker run --network host ${env_exporter_variables} -it hdsentinel_exporter
