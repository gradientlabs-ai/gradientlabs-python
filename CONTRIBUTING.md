## Project setup

This library uses Poetry, which can be installed via:

```bash
brew install poetry
```

And then you can set up a virtual environment for this library with:

```bash
poetry install
```

## Running the examples

This library uses Poetry, which can be installed via:

```bash
make run
```

## Publishing a new version

- Update the version number in [`pyproject.toml`](./pyproject.toml)
- Tag the version `git tag vX.X.X`
- Push the tag `git push origin vX.X.X`
- Wait for the GitHub [machinery](https://github.com/gradientlabs-ai/python-client/actions/workflows/publish.yaml) to do its magic
