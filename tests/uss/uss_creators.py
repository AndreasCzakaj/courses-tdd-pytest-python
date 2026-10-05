"""The "creators" return valid objects.

A test then breaks them in 1 place, so it tests for 1 error.
"""

from dataclasses import replace
from datetime import datetime, timezone

from uss.account import Account
from uss.password import hash_password

VALID_PASSWORD = "Correct-Horse_42"
VALID_BUT_WRONG_PASSWORD = "Battery.Staple+7"

# hashing is slow on purpose => once for all tests
VALID_PASSWORD_HASH = hash_password(VALID_PASSWORD)


def create_verified_account() -> Account:
    return Account(
        id="0b0e7a4c-8d2f-4c3a-9a51-6f1f3c1d2e01",
        username="alice_verified",
        password_hash=VALID_PASSWORD_HASH,
        email="alice@example.com",
        tc_accepted=datetime(2026, 10, 1, 8, 0, tzinfo=timezone.utc),
        status="verified",
    )


def create_not_verified_account() -> Account:
    return replace(
        create_verified_account(),
        id="0b0e7a4c-8d2f-4c3a-9a51-6f1f3c1d2e02",
        username="bob_not_verified",
        email="bob@example.com",
        status="new",
    )


def create_valid_credentials() -> dict:
    return {"username": create_verified_account().username, "password": VALID_PASSWORD}


def create_valid_credentials_not_verified_account() -> dict:
    return {"username": create_not_verified_account().username, "password": VALID_PASSWORD}


def create_valid_credentials_unknown_user() -> dict:
    return {"username": "idonotexist", "password": VALID_PASSWORD}


def create_expected_session_json() -> dict:
    account = create_verified_account()
    return {"accountId": account.id, "username": account.username, "email": account.email}
