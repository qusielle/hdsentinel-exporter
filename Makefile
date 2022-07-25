SHELL := /bin/bash

.PHONY: autopep
autopep:
	autopep8 -aaaa --exit-code --in-place --max-line-length 99 --recursive .

.PHONY: flake8
flake8:
	flake8 --max-line-length 99 .

.PHONY: mypy
mypy:
	mypy .

.PHONY: lint
lint: autopep flake8 mypy

.PHONY: test
test:
	python -m pytest -vv .

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
