import logging

import pytest

from uss.account_dao import AccountDaoThrowingImpl
from uss.controller_utils import MESSAGE_SERVER_ERROR
from uss.login_controller import LoginController
from uss_creators import (
    VALID_BUT_WRONG_PASSWORD,
    create_expected_session_json,
    create_valid_credentials,
    create_valid_credentials_not_verified_account,
    create_valid_credentials_unknown_user,
)

MESSAGE_LOGIN_ERROR = "unknown username or wrong password"


@pytest.fixture
def ctrl(service) -> LoginController:
    return LoginController(service)


@pytest.mark.parametrize(
    "body, status, error",
    [
        pytest.param(None, 400, "invalid: username", id="no body"),
        pytest.param({**create_valid_credentials(), "username": "al"}, 400, "invalid: username", id="invalid username"),
        pytest.param(
            {**create_valid_credentials(), "password": "pwd"}, 400, "invalid: password", id="invalid password"
        ),
        pytest.param(create_valid_credentials_unknown_user(), 401, MESSAGE_LOGIN_ERROR, id="no such username"),
        pytest.param(
            {**create_valid_credentials(), "password": VALID_BUT_WRONG_PASSWORD},
            401,
            MESSAGE_LOGIN_ERROR,
            id="wrong password",
        ),
        pytest.param(
            create_valid_credentials_not_verified_account(), 400, "account not verified", id="account not verified"
        ),
    ],
)
def test_client_errors(ctrl, body, status, error):
    assert ctrl.action(body) == ({"error": error}, status)


def test_500_database_not_available(ctrl, service, caplog):
    # given
    service.account_dao = AccountDaoThrowingImpl()

    # when
    with caplog.at_level(logging.ERROR):
        actual = ctrl.action(create_valid_credentials())

    # then: the client gets no details, the log does
    assert actual == ({"error": MESSAGE_SERVER_ERROR}, 500)
    assert "Database not available" in caplog.text


def test_200_session(ctrl):
    assert ctrl.action(create_valid_credentials()) == (create_expected_session_json(), 200)
