"""All parts together: HTTP => Flask => controller => service => SQLite.

The details of each scenario are covered by the (much faster) unit tests.
"""

import pytest

from uss.account_dao_sqlite_impl import AccountDaoSqliteImpl
from uss.server import create_app
from uss_creators import (
    VALID_BUT_WRONG_PASSWORD,
    create_expected_session_json,
    create_not_verified_account,
    create_valid_credentials,
    create_valid_credentials_not_verified_account,
    create_valid_credentials_unknown_user,
    create_verified_account,
)


@pytest.fixture
def client(tmp_path):
    """Flask's test client for the app, with a real SQLite database in a temporary folder"""
    db_path = str(tmp_path / "uss.db")
    dao = AccountDaoSqliteImpl(db_path)
    dao.create_table()
    dao.save(create_verified_account())
    dao.save(create_not_verified_account())

    return create_app(db_path).test_client()


@pytest.mark.parametrize(
    "body, expected",
    [
        pytest.param({}, 400, id="credentials have invalid syntax"),
        pytest.param(create_valid_credentials_unknown_user(), 401, id="no such username"),
        pytest.param({**create_valid_credentials(), "password": VALID_BUT_WRONG_PASSWORD}, 401, id="wrong password"),
        pytest.param(create_valid_credentials_not_verified_account(), 400, id="account not verified"),
    ],
)
def test_post_login_errors(client, body, expected):
    response = client.post("/uss/login", json=body)

    assert response.status_code == expected
    assert list(response.get_json()) == ["error"]


def test_post_login_400_no_body_at_all(client):
    response = client.post("/uss/login")

    assert response.status_code == 400


def test_post_login_400_no_json(client):
    response = client.post("/uss/login", data="nonsense", content_type="application/json")

    assert response.status_code == 400


def test_post_login_200_and_session(client):
    response = client.post("/uss/login", json=create_valid_credentials())

    assert response.status_code == 200
    assert response.get_json() == create_expected_session_json()
