from funwithflags.uuid_generator import UuidGenerator

# Decorator pattern: a decorator IS a UuidGenerator and HAS a UuidGenerator.
# It delegates the work and adds its own functionality to the result.
# (not to be confused with Python's `@decorator` syntax, which decorates functions)


class UuidGeneratorUpperCaseDecoratorImpl(UuidGenerator):
    def __init__(self, delegate: UuidGenerator):
        self._delegate = delegate

    def create(self) -> str:
        return self._delegate.create().upper()


class UuidGeneratorWithDashesDecoratorImpl(UuidGenerator):
    def __init__(self, delegate: UuidGenerator):
        self._delegate = delegate

    def create(self) -> str:
        uuid = self._delegate.create()
        return "-".join([uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]])
