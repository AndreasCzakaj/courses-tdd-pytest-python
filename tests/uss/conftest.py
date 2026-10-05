import pytest

from uss.account_dao import AccountDaoDictImpl
from uss.user_self_service import UserSelfService
from uss_creators import create_not_verified_account, create_verified_account


@pytest.fixture
def service() -> UserSelfService:
    """A service with working dependencies: 1 verified and 1 not verified account"""
    account_dao = AccountDaoDictImpl([create_verified_account(), create_not_verified_account()])
    return UserSelfService(account_dao)
