import pytest

from uss.account import UserSession
from uss.account_dao import AccountDaoThrowingImpl
from uss.user_self_service import AccountNotVerifiedError, AuthenticationError, ServerError
from uss.validation import ValidationError
from uss_creators import (
    VALID_BUT_WRONG_PASSWORD,
    create_valid_credentials,
    create_valid_credentials_not_verified_account,
    create_valid_credentials_unknown_user,
    create_verified_account,
)


def test_if_i_pass_no_credentials_there_should_be_a_validation_error(service):
    with pytest.raises(ValidationError, match="^invalid: username$"):
        service.login(None)


def test_if_i_pass_syntactically_invalid_credentials_there_should_be_a_validation_error(service):
    # given
    credentials = {**create_valid_credentials(), "password": "tooshort"}

    # when, then
    with pytest.raises(ValidationError, match="^invalid: password$"):
        service.login(credentials)


def test_if_i_dont_have_an_account_there_should_be_a_login_error(service):
    # given
    credentials = create_valid_credentials_unknown_user()

    # when, then
    with pytest.raises(AuthenticationError, match="^unknown username or wrong password$"):
        service.login(credentials)


def test_if_i_dont_pass_the_right_password_there_should_be_the_same_login_error(service):
    # given
    credentials = {**create_valid_credentials(), "password": VALID_BUT_WRONG_PASSWORD}

    # when, then
    with pytest.raises(AuthenticationError, match="^unknown username or wrong password$"):
        service.login(credentials)


def test_if_my_account_is_not_verified_yet_there_should_be_an_error(service):
    # given
    credentials = create_valid_credentials_not_verified_account()

    # when, then
    with pytest.raises(AccountNotVerifiedError, match="^account not verified$"):
        service.login(credentials)


def test_if_my_account_is_not_verified_and_the_password_is_wrong_there_should_be_the_login_error(service):
    # given
    credentials = {**create_valid_credentials_not_verified_account(), "password": VALID_BUT_WRONG_PASSWORD}

    # when, then: the status of an account is none of a stranger's business
    with pytest.raises(AuthenticationError):
        service.login(credentials)


def test_if_the_database_does_not_work_then_i_should_get_an_appropriate_error(service):
    # given
    service.account_dao = AccountDaoThrowingImpl()
    credentials = create_valid_credentials()

    # when, then
    with pytest.raises(ServerError, match="^Database not available. Try later.$"):
        service.login(credentials)


def test_if_i_pass_valid_credentials_of_a_verified_account_then_i_get_a_session(service):
    # given
    credentials = create_valid_credentials()
    account = create_verified_account()

    # when
    actual = service.login(credentials)

    # then: exactly these fields, e.g. no password hash
    assert actual == UserSession(account_id=account.id, username=account.username, email=account.email)
