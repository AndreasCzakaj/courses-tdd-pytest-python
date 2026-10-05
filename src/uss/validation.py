import re

from uss.account import Credentials


class ValidationError(Exception):
    def __init__(self, field: str):
        super().__init__(f"invalid: {field}")
        self.field = field


# The validation functions return the valid value, so the caller gets it with the right type.
# `fullmatch`: with `match` and `$`, a trailing newline would be accepted.

REGEX_USERNAME = re.compile(r"[a-zA-Z0-9\-_]{8,20}")
REGEX_PASSWORD = re.compile(r"[a-zA-Z0-9\-_.,+]{12,32}")


def validate_username(username: object) -> str:
    return _validate(username, REGEX_USERNAME, "username")


def validate_password(password: object) -> str:
    return _validate(password, REGEX_PASSWORD, "password")


def validate_credentials(credentials: object) -> Credentials:
    # the input is untrusted: it may be anything, e.g. the body of an HTTP request
    data = credentials if isinstance(credentials, dict) else {}
    return Credentials(
        username=validate_username(data.get("username")),
        password=validate_password(data.get("password")),
    )


def _validate(value: object, regex: re.Pattern[str], field: str) -> str:
    if isinstance(value, str) and regex.fullmatch(value):
        return value
    raise ValidationError(field)
