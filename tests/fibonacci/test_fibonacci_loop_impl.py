import pytest

from fibonacci.fibonacci import Fibonacci, FibonacciLoopImpl
from fibonacci_contract import FibonacciContract


class TestFibonacciLoopImpl(FibonacciContract):
    @pytest.fixture
    def fibonacci(self) -> Fibonacci:
        return FibonacciLoopImpl()

    @pytest.mark.parametrize(
        "index, expected",
        [
            (30, 832_040),
            (40, 102_334_155),
            (46, 1_836_311_903),
        ],
    )
    def test_should_pass_for_large_numbers(self, fibonacci, index, expected):
        assert fibonacci.calculate(index) == expected
