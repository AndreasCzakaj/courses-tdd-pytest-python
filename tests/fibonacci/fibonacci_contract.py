import pytest

from fibonacci.fibonacci import Fibonacci

# see https://www.wackerart.de/mathematik/big_numbers/fibonacci_numbers.html


class FibonacciContract:
    """Reusable tests: every implementation of `Fibonacci` must pass them.

    Not collected by pytest itself: neither the file name starts with `test_`
    nor the class name with `Test`. The subclasses are.
    """

    @pytest.fixture
    def fibonacci(self) -> Fibonacci:
        raise NotImplementedError("override me in the subclass")

    @pytest.mark.parametrize(
        "index, expected",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (6, 8),
            (10, 55),
            (19, 4_181),
            (20, 6_765),
        ],
    )
    def test_should_pass_for_small_numbers(self, fibonacci, index, expected):
        actual = fibonacci.calculate(index)
        assert actual == expected

    @pytest.mark.parametrize(
        "index, expected",
        [
            pytest.param(None, "index must not be None", id="None"),
            pytest.param(-1, "index must not be negative", id="negative"),
            pytest.param(47, "index must not be > 46", id="above 46"),
        ],
    )
    def test_should_fail(self, fibonacci, index, expected):
        with pytest.raises(ValueError) as error:
            fibonacci.calculate(index)
        assert str(error.value) == expected
