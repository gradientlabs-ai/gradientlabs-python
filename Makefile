.PHONY: fmt test

fmt:
	@poetry run black ./

test:
	@poetry run pytest tests
