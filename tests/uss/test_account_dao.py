import pytest

from uss.account_dao import AccountDaoDictImpl, AccountDaoThrowingImpl, DaoError
from uss_creators import create_verified_account


def test_dict_impl_should_find_an_account_by_its_username():
    account = create_verified_account()
    dao = AccountDaoDictImpl([account])

    assert dao.find_by_username(account.username) == account


def test_dict_impl_should_return_none_for_an_unknown_username():
    dao = AccountDaoDictImpl()

    assert dao.find_by_username("idonotexist") is None


def test_throwing_impl_should_raise_a_dao_error():
    dao = AccountDaoThrowingImpl()

    with pytest.raises(DaoError, match="^find_by_username: oops$"):
        dao.find_by_username("anyone")
