from abc import ABC, abstractmethod
from collections.abc import Iterable

from uss.account import Account


class AccountDao(ABC):
    """An interface on purpose: the service is isolated from the database,
    and the implementations are interchangeable."""

    @abstractmethod
    def find_by_username(self, username: str) -> Account | None: ...


class DaoError(Exception):
    pass


class AccountDaoDictImpl(AccountDao):
    def __init__(self, accounts: Iterable[Account] = ()):
        self._repo = {account.username: account for account in accounts}

    def find_by_username(self, username: str) -> Account | None:
        return self._repo.get(username)


class AccountDaoThrowingImpl(AccountDao):
    def find_by_username(self, username: str) -> Account | None:
        raise DaoError("find_by_username: oops")
