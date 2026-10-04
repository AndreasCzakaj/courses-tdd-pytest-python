import re
from collections import Counter

import pytest

from funwithflags.uuid_generator import UuidGenerator, UuidGeneratorNaiveRandomImpl

base_impl = UuidGeneratorNaiveRandomImpl()


@pytest.mark.parametrize(
    "uuid_generator, expected_regex",
    [
        pytest.param(base_impl, "[a-f0-9]{32}", id="lower case, no dashes"),
        # pytest.param(???, "[A-F0-9]{32}", id="upper case, no dashes"),
        # pytest.param(
        #     ???, "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", id="lower case, with dashes"),
        # pytest.param(
        #     ???, "[A-F0-9]{8}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{12}", id="upper case, with dashes"),
    ],
)
def test_should_create_a_uuid_in_the_matching_format(uuid_generator: UuidGenerator, expected_regex: str):
    # when
    actual = uuid_generator.create()

    # then
    assert re.fullmatch(expected_regex, actual)


def test_should_use_all_chars():
    hex_chars = set("0123456789abcdef")
    found_chars = Counter()

    uuid_generator = UuidGeneratorNaiveRandomImpl()

    # yes, I'm looping. I need this because the process is random.
    for _ in range(10):
        found_chars.update(uuid_generator.create())

    assert set(found_chars) == hex_chars
    assert all(count > 0 for count in found_chars.values())
