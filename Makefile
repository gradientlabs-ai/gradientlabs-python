.PHONY: fmt test run install

fmt:
	@poetry run black ./

test:
	@poetry run pytest tests

run:
	@poetry run python examples/run.py

install:
	@poetry install
