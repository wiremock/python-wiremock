# Contributing to Python WireMock

[![a](https://img.shields.io/badge/slack-%23wiremock%2Fpython-brightgreen?style=flat&logo=slack)](https://slack.wiremock.org/)

WireMock exists and continues to thrive due to the efforts of over 150 contributors, and we continue to welcome contributions to its evolution. Regardless of your expertise and time you could dedicate, there’re opportunities to participate and help the project!

This page covers contributing to _Python WireMock_.
For generic guidelines and links to other technology stacks,
see [this page](https://wiremock.org/docs/participate/).

## Get Started

1. Join us ion the `#wiremock-python` channel on the [WireMock Slack](https://slack.wiremock.org/)
2. Check out the GitHub issues!

## Pull Requests

All patches to the repository are done via pull requests.
No special prerequisites exist, you can just submit the patches!
General expectations:

- All Tests and static checkers must pass
- Code coverage shouldn't decrease
- All Pull Requests should be rebased against master **before** submitting the PR.
- The Pull Request titles represent the change well for users or developers

## Development

We use [Poetry](https://python-poetry.org/) for packaging and dependency management.

After forking and cloning the repository,
run the following command to setup the project:

`poetry install`

Then use your favorite IDE for development and testing.

## Contributing examples

Please submit new examples as a pull requests to the
[examples directory](https://github.com/wiremock/python-wiremock/tree/master/examples). 
You can also also add links to external examples and tutorials to the `README.md`
file in the directory.

When adding new examples,
make sure to update the [documentation site page](./examples.md) too.

## Working on Documentation

The documentation is powered by [MkDocs](https://www.mkdocs.org/) and [ReadTheDocs](https://readthedocs.org/).
All the necessary dependencies are included into the Poetry definition.
To build the docs locally:

```bash
poetry run mkdocs build --site-dir=html
```

MkDocs also comes with a built-in dev-server that lets you preview your documentation as you work on it by running the `mkdocs serve` command.
By default, it will deploy the live documentation site to `http://localhost:8000`.

## See also

- [Contributing to WireMock](https://wiremock.org/docs/participate/)
