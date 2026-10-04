# The image of the "app": prints a new UUID
#   docker build -f Dockerfile.app -t tdd-pytest-python .
#   docker run --rm tdd-pytest-python
FROM python:3.12-slim
WORKDIR /app
# production code only: no tests, no dev dependencies
COPY src/ ./
USER nobody
ENTRYPOINT ["python", "-m", "funwithflags"]
