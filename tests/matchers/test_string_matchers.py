import re

import pytest
from pytest_check import check

from matchers.first import First


@pytest.fixture
def email() -> str:
    return First().get_email()


@pytest.mark.skip(reason="email should not be None")
def test_should_not_be_none(email):
    pass


@pytest.mark.skip(reason="email should be a string")
def test_should_be_a_string(email):
    pass


@pytest.mark.skip(reason="email should be andreas.czakaj@binary-stars.eu")
def test_should_be_andreas_czakaj(email):
    pass


@pytest.mark.skip(reason="email should start with 'andreas'")
def test_should_start_with_andreas(email):
    pass


@pytest.mark.skip(reason="email should end with '.eu'")
def test_should_end_with_dot_eu(email):
    pass


@pytest.mark.skip(reason="email should not end with '.com'")
def test_should_not_end_with_dot_com(email):
    pass


@pytest.mark.skip(reason="email should contain 'binary'")
def test_should_contain_binary(email):
    pass


@pytest.mark.skip(reason="email should contain 'andreas' and 'stars'")
def test_should_contain_andreas_and_stars(email):
    pass


@pytest.mark.skip(reason="email should match regular expression '[a-z.@\\-]+'")
def test_should_match_regex(email):
    pass


@pytest.mark.skip(reason="TODO: all of the above in 1 test ... and try not to exit at the 1st failure")
def test_should_match_all_in_one(email):
    pass
