import re

import pytest
from pytest_check import check

from matchers.first import First


@pytest.fixture
def email() -> str:
    return First().get_email()


def test_should_not_be_none(email):
    assert email is not None


def test_should_be_a_string(email):
    assert isinstance(email, str)


def test_should_be_andreas_czakaj(email):
    assert email == "andreas.czakaj@binary-stars.eu"
    # ignoring case
    assert email.casefold() == "ANDREAS.czakaj@binary-stars.eu".casefold()


def test_should_start_with_andreas(email):
    assert email.startswith("andreas")


def test_should_end_with_dot_eu(email):
    assert email.endswith(".eu")


def test_should_not_end_with_dot_com(email):
    assert not email.endswith(".com")


def test_should_contain_binary(email):
    assert "binary" in email


def test_should_contain_andreas_and_stars(email):
    assert "andreas" in email and "stars" in email
    # alternative: scales better and still is 1 expression
    assert all(part in email for part in ("andreas", "stars"))


def test_should_match_regex(email):
    # the 2nd arg of `assert` is the message, like AssertJ's `.as(...)`
    assert re.fullmatch(r"[0-9a-z.@\-]+", email), "it should match super simplistic reg exp"


def test_should_match_all_in_one(email):
    # conditions can be combined with `and`
    # ... however, the test will stop at the first error
    assert (
        email is not None
        and email == "andreas.czakaj@binary-stars.eu"
        and email.startswith("andreas")
        and email.endswith(".eu")
        and not email.endswith(".com")
        and "binary" in email
        and re.fullmatch(r"[0-9a-z.@\-]+", email)
    )

    # to prevent this, you can use "soft assertions" from the plugin `pytest-check`:
    # all checks are executed, all failures are reported
    with check:
        assert email is not None
    with check:
        assert email == "andreas.czakaj@binary-stars.eu"
    with check:
        assert email.startswith("andreas")
    with check:
        assert email.endswith(".eu")
    with check:
        assert not email.endswith(".com")
    with check:
        assert "binary" in email
    with check:
        assert re.fullmatch(r"[0-9a-z.@\-]+", email)
