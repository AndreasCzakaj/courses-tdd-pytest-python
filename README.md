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

On branch `main`, the pipeline is RED by design: the linter rejects the legacy code in
`src/uss_dirty` (complexity), and the first test must fail.
On branch `solution` it is GREEN.

Run the steps locally:

``` Bash
ruff check .
pytest --cov --cov-fail-under=90
docker build -f Dockerfile.app -t tdd-pytest-python .
docker run --rm tdd-pytest-python
```

# User Self Service: Login (`src/uss_dirty`)

`src/uss_dirty/server.py` implements the login. It works, but everything happens in the
handler of the route `/uss/login`: validation, database calls, error handling.
There are no tests.

Scenarios:

* Credentials (username + password) have invalid syntax => 400
  * username: min 8, max 20 chars; `[a-zA-Z0-9\-_]`
  * password: min 12, max 32 chars; `[a-zA-Z0-9\-_.,+]`
* Credentials have valid syntax, but no such username => 401
* Username exists, but wrong password => SAME(!) error 401
* Credentials OK, but account status is not "verified" => 400
* All OK => 200 + session object including account ID, username, email

## Your task

* Extract functions and classes
* Separate Operation code (logic: validation, password check, decisions) from
  Integration code (HTTP, database)
* Add tests along the way
* Done when: all scenarios are covered by tests, and `ruff check .` is green
  (now: "`login` is too complex (14 > 5)")

## Run it

``` Bash
cd src
python -m uss_dirty             # SQLite database + some accounts, see the console output
PORT=3055 python -m uss_dirty   # if port 3000 is taken
```

``` Bash
curl -i -X POST localhost:3000/uss/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "alice_verified", "password": "Correct-Horse_42"}'
```

# Folder structure

```
src/                    production code
  hello.py
  matchers/
  fibonacci/
  funwithflags/           "Fun With Flags": decorator pattern
  uss_dirty/              "User Self Service: Login": legacy code task
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
