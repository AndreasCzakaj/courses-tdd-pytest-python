import pytest

from matchers.first import First


@pytest.fixture
def first() -> First:
    return First()


@pytest.fixture
def items(first) -> list[str]:
    return first.get_list()


@pytest.fixture
def mapping(first) -> dict[str, str]:
    return first.map


def test_should_contain_3_elements(items):
    assert len(items) == 3


def test_should_contain_a(items):
    assert "a" in items


def test_should_not_contain_d(items):
    assert "d" not in items


def test_should_contain_c_and_a(items):
    assert {"c", "a"} <= set(items)  # "is subset of"


def test_should_not_contain_duplicates(items):
    assert len(items) == len(set(items))


def test_more(items):
    # precisely: same items, same order
    assert items == ["a", "b", "c"]
    # loosely: same items, any order
    assert sorted(items) == sorted(["c", "a", "b"])
    # contains any of
    assert set(items) & {"c", "a", "b", "d"}


def test_map(mapping):
    assert "k1" in mapping
    assert "xxx" not in mapping
    assert "v2" in mapping.values()
    assert "yyy" not in mapping.values()
    assert mapping["k2"] == "v2"
    # alternative for key + value: "is subset of"
    assert {"k2": "v2"}.items() <= mapping.items()
