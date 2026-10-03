import pytest

from fibonacci.fibonacci import FibonacciLoopImpl, FibonacciRecursionImpl

# The other way to reuse tests, w/out inheritance: a parameterized fixture.
# Every test that uses the fixture runs once per implementation.


@pytest.fixture(params=[FibonacciLoopImpl, FibonacciRecursionImpl])
def fibonacci(request):
    return request.param()


@pytest.mark.parametrize("index, expected", [(0, 0), (1, 1), (2, 1), (6, 8), (19, 4_181)])
def test_should_yield_expected_for_index(fibonacci, index, expected):
    assert fibonacci.calculate(index) == expected
