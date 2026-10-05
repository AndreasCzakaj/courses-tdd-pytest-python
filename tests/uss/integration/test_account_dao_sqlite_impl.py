import pytest

from uss.account_dao import DaoError
from uss.account_dao_sqlite_impl import AccountDaoSqliteImpl
from uss_creators import create_not_verified_account, create_verified_account


@pytest.fixture
def dao(tmp_path) -> AccountDaoSqliteImpl:
    """A DAO with a real SQLite database in a temporary folder"""
    dao = AccountDaoSqliteImpl(str(tmp_path / "uss.db"))
    dao.create_table()
    return dao


def test_should_find_an_account_by_its_username(dao):
    # given
    account = create_verified_account()
    dao.save(account)
    dao.save(create_not_verified_account())

    # when
    actual = dao.find_by_username(account.username)

    # then: the account as it was saved
    assert actual == account


def test_should_return_none_for_an_unknown_username(dao):
    assert dao.find_by_username("idonotexist") is None


def test_should_not_save_the_same_username_twice(dao):
    dao.save(create_verified_account())

    with pytest.raises(DaoError, match="^SQLite Error$"):
        dao.save(create_verified_account())


def test_should_raise_a_dao_error_if_the_database_is_not_available(tmp_path):
    # given: a folder is not a database file
    dao = AccountDaoSqliteImpl(str(tmp_path))

    # when, then
    with pytest.raises(DaoError, match="^SQLite Error$"):
        dao.find_by_username("alice_verified")
