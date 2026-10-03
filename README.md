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
pyproject.toml          pytest configuration
requirements.txt        dependencies
```
