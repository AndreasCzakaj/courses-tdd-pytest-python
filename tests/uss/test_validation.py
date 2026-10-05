import pytest

from uss.account import Credentials
from uss.validation import ValidationError, validate_credentials, validate_password, validate_username
from uss_creators import (
    VALID_BUT_WRONG_PASSWORD,
    VALID_PASSWORD,
    create_valid_credentials,
    create_valid_credentials_not_verified_account,
    create_valid_credentials_unknown_user,
)


@pytest.mark.parametrize(
    "given",
    [
        pytest.param(None, id="None"),
        pytest.param("", id="empty"),
        pytest.param("        ", id="empty whitespace"),
        pytest.param(12345678, id="not a string"),
        pytest.param({"$ne": ""}, id="a dict (NoSQL injection)"),
        pytest.param("1234567", id="too short"),
        pytest.param("1234567 ", id="too short with padding"),
        pytest.param("123456789012345678901", id="too long"),
        pytest.param("1234 6789", id="invalid char: blank"),
        pytest.param("1234.6789", id="invalid char: allowed in passwords only"),
        pytest.param("12345678\n", id="trailing newline"),
    ],
)
def test_validate_username_should_fail(given):
    with pytest.raises(ValidationError, match="^invalid: username$"):
        validate_username(given)


@pytest.mark.parametrize(
    "given",
    [
        pytest.param("12345678", id="min size"),
        pytest.param("12345678901234567890", id="max size"),
        pytest.param("aZ09-_aZ", id="all allowed chars"),
        pytest.param(create_valid_credentials()["username"], id="create_valid_credentials"),
        pytest.param(create_valid_credentials_unknown_user()["username"], id="create_valid_credentials_unknown_user"),
    ],
)
def test_validate_username_should_pass(given):
    assert validate_username(given) == given


@pytest.mark.parametrize(
    "given",
    [
        pytest.param(None, id="None"),
        pytest.param("", id="empty"),
        pytest.param("            ", id="empty whitespace"),
        pytest.param(123456789012, id="not a string"),
        pytest.param("12345678901", id="too short"),
        pytest.param("12345678901 ", id="too short with padding"),
        pytest.param("123456789012345678901234567890123", id="too long"),
        pytest.param("123456 89012", id="invalid char: blank"),
        pytest.param("123456!89012", id="invalid char: !"),
        pytest.param("123456789012\n", id="trailing newline"),
    ],
)
def test_validate_password_should_fail(given):
    with pytest.raises(ValidationError, match="^invalid: password$"):
        validate_password(given)


@pytest.mark.parametrize(
    "given",
    [
        pytest.param("123456789012", id="min size"),
        pytest.param("12345678901234567890123456789012", id="max size"),
        pytest.param("aZ09-_.,+aZ0", id="all allowed chars"),
        pytest.param(VALID_PASSWORD, id="VALID_PASSWORD"),
        pytest.param(VALID_BUT_WRONG_PASSWORD, id="VALID_BUT_WRONG_PASSWORD"),
    ],
)
def test_validate_password_should_pass(given):
    assert validate_password(given) == given


@pytest.mark.parametrize(
    "given, field",
    [
        pytest.param(None, "username", id="None"),
        pytest.param({}, "username", id="empty dict"),
        pytest.param("alice_verified", "username", id="not a dict"),
        pytest.param([create_valid_credentials()], "username", id="a list"),
        pytest.param({**create_valid_credentials(), "username": "al"}, "username", id="invalid username"),
        pytest.param({**create_valid_credentials(), "password": "pwd"}, "password", id="invalid password"),
        pytest.param({"username": "al", "password": "pwd"}, "username", id="both invalid: reports the 1st one"),
    ],
)
def test_validate_credentials_should_fail(given, field):
    with pytest.raises(ValidationError) as error:
        validate_credentials(given)
    assert error.value.field == field


@pytest.mark.parametrize(
    "given",
    [
        pytest.param(create_valid_credentials(), id="create_valid_credentials"),
        pytest.param(
            create_valid_credentials_not_verified_account(), id="create_valid_credentials_not_verified_account"
        ),
        pytest.param(create_valid_credentials_unknown_user(), id="create_valid_credentials_unknown_user"),
    ],
)
def test_validate_credentials_should_pass(given):
    assert validate_credentials(given) == Credentials(**given)


def test_the_error_should_name_the_invalid_field():
    error = ValidationError("username")

    assert error.field == "username"
    assert str(error) == "invalid: username"
