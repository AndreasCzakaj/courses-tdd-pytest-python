import pytest

from fibonacci.fibonacci import Fibonacci, FibonacciRecursionImpl
from fibonacci_contract import FibonacciContract


class TestFibonacciRecursionImpl(FibonacciContract):
    @pytest.fixture
    def fibonacci(self) -> Fibonacci:
        return FibonacciRecursionImpl()
