from abc import ABC, abstractmethod


class Fibonacci(ABC):
    def calculate(self, index: int) -> int:
        self._check(index)

        if index < 2:
            return index

        return self._calculate_internal(index)

    @abstractmethod
    def _calculate_internal(self, index: int) -> int: ...

    def _check(self, index: int) -> None:
        if index is None:
            raise ValueError("index must not be None")
        if index < 0:
            raise ValueError("index must not be negative")
        if index > 46:
            raise ValueError("index must not be > 46")


class FibonacciLoopImpl(Fibonacci):
    def _calculate_internal(self, index: int) -> int:
        previous_previous = 0
        previous = 1
        result = 0
        for _ in range(2, index + 1):
            result = previous + previous_previous
            previous_previous = previous
            previous = result
        return result


class FibonacciRecursionImpl(Fibonacci):
    def _calculate_internal(self, index: int) -> int:
        return self.calculate(index - 2) + self.calculate(index - 1)
