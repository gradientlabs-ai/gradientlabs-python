VERSION = $(shell poetry version | rev | cut -d ' ' -f 1)

.PHONY: fmt test run install release

fmt:
	@poetry run black ./

test:
	@poetry run pytest tests

run:
	@poetry run python examples/run.py

install:
	@poetry install

release: 
	@echo Shipping version ${VERSION}
	@git tag v${VERSION}
	@git push origin v${VERSION}
