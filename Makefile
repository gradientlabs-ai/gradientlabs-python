.PHONY: fmt test run

fmt:
	@poetry run black ./

test:
	@poetry run pytest tests

run:
	@poetry run python examples/run.py
