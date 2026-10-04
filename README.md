# TDD with pytest

Branch `main` contains the exercises, branch `solution` contains the solutions.

# Initially, after cloning

``` Bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

# Daily use

## Run tests once

``` Bash
pytest
```

## Run tests continuously ("watch mode"), TDD style

``` Bash
ptw .
```

## Run tests once, with coverage

``` Bash
pytest --cov --cov-report=term-missing
```

## Run a subset

``` Bash
pytest tests/test_hello.py                  # one file
pytest tests/matchers                       # one folder
pytest -k "starts_with"                     # by name
pytest -v                                   # verbose: 1 line per test
```

## Lint: code style, likely bugs, cyclomatic complexity

``` Bash
ruff check .
```

# CI/CD

`.gitlab-ci.yml` defines the GitLab pipeline: lint => test => package

* **lint**: `ruff check .`, any violation breaks the build (rules: `pyproject.toml`)
* **test**: all tests with coverage, less than 90% breaks the build
* **package**: builds the Docker image of the "app" (`Dockerfile.app`), which prints a UUID

On branch `main`, the pipeline is RED by design: the first test must fail.
On branch `solution` it is GREEN.

Run the steps locally:

``` Bash
ruff check .
pytest --cov --cov-fail-under=90
docker build -f Dockerfile.app -t tdd-pytest-python .
docker run --rm tdd-pytest-python
```

# Folder structure

```
src/                    production code
  hello.py
  matchers/
  fibonacci/
  funwithflags/           "Fun With Flags": decorator pattern
tests/                  test code, files must be named test_*.py
  test_hello.py
  matchers/
  fibonacci/
  funwithflags/
pyproject.toml          configuration of pytest, coverage, ruff
.gitlab-ci.yml          CI/CD pipeline
Dockerfile.app          Docker image of the "app"
requirements.txt        dependencies
```
