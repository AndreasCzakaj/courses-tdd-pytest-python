from abc import ABC, abstractmethod
from secrets import randbelow


class UuidGenerator(ABC):
    @abstractmethod
    def create(self) -> str: ...


class UuidGeneratorNaiveRandomImpl(UuidGenerator):
    def create(self) -> str:
        return "".join(self._create_one() for _ in range(32))

    def _create_one(self) -> str:
        return format(randbelow(16), "x")
