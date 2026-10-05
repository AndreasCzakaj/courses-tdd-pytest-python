import pytest

from uss.account_dao import DaoError
from uss.controller_utils import MESSAGE_SERVER_ERROR, calc_error_message, calc_http_error_code
from uss.user_self_service import AccountNotVerifiedError, AuthenticationError, ServerError
from uss.validation import ValidationError


@pytest.mark.parametrize(
    "error, expected",
    [
        pytest.param(ValidationError("username"), 400, id="invalid input is the client's fault"),
        pytest.param(AuthenticationError(), 401, id="unknown username or wrong password"),
        pytest.param(AccountNotVerifiedError(), 400, id="account not verified"),
        pytest.param(ServerError("oops"), 500, id="a server error is our fault"),
        pytest.param(DaoError("oops"), 500, id="any other error is our fault"),
        pytest.param(ZeroDivisionError(), 500, id="anything else is our fault"),
    ],
)
def test_should_map_to_http_status(error, expected):
    assert calc_http_error_code(error) == expected


@pytest.mark.parametrize(
    "error, expected",
    [
        pytest.param(ValidationError("username"), "invalid: username", id="names the invalid field"),
        pytest.param(AuthenticationError(), "unknown username or wrong password", id="does not reveal which one"),
        pytest.param(AccountNotVerifiedError(), "account not verified", id="account not verified"),
        pytest.param(ServerError("db is down"), MESSAGE_SERVER_ERROR, id="server error: hides the internals"),
        pytest.param(DaoError("SQLite Error"), MESSAGE_SERVER_ERROR, id="dao error: hides the internals"),
        pytest.param(ZeroDivisionError("oops"), MESSAGE_SERVER_ERROR, id="other error: hides the internals"),
    ],
)
def test_should_map_to_message(error, expected):
    assert calc_error_message(error) == expected
