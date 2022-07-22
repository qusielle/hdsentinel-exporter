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
