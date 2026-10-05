import re

import pytest

from uss.password import hash_password, verify_password
from uss_creators import VALID_BUT_WRONG_PASSWORD, VALID_PASSWORD

SALT = "00112233445566778899aabbccddeeff"
PASSWORD_HASH = hash_password(VALID_PASSWORD, SALT)


def test_hash_should_be_salt_and_hash_hex_encoded():
    assert re.fullmatch(r"[a-f0-9]{32}:[a-f0-9]{128}", hash_password(VALID_PASSWORD))


def test_hash_should_not_contain_the_password():
    assert VALID_PASSWORD not in hash_password(VALID_PASSWORD)


def test_hash_should_be_reproducible_for_the_same_salt():
    assert hash_password(VALID_PASSWORD, SALT) == hash_password(VALID_PASSWORD, SALT)


def test_hash_should_use_a_new_salt_each_time():
    # same password, different hashes
    assert hash_password(VALID_PASSWORD) != hash_password(VALID_PASSWORD)


def test_verify_should_accept_the_right_password():
    assert verify_password(VALID_PASSWORD, PASSWORD_HASH) is True


@pytest.mark.parametrize(
    "password, given",
    [
        pytest.param(VALID_BUT_WRONG_PASSWORD, PASSWORD_HASH, id="wrong password"),
        pytest.param("", PASSWORD_HASH, id="empty password"),
        pytest.param(VALID_PASSWORD, SALT, id="stored value w/out hash"),
        pytest.param(VALID_PASSWORD, "", id="stored value empty"),
        pytest.param(VALID_PASSWORD, PASSWORD_HASH[:-1], id="stored hash truncated"),
    ],
)
def test_verify_should_reject(password, given):
    assert verify_password(password, given) is False
