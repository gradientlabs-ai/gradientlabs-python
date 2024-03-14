## Project setup



## Publishing a new version

- Update the version number in [`pyproject.toml`](./pyproject.toml)
- Tag the version `git tag vX.X.X`
- Push the tag `git push origin vX.X.X`
- Wait for the GitHub [machinery](https://github.com/gradientlabs-ai/python-client/actions/workflows/publish.yaml) to do its magic
