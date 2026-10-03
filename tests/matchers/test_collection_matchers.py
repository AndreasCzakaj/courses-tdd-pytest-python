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


@pytest.mark.skip(reason="list should contain 3 elements")
def test_should_contain_3_elements(items):
    pass


@pytest.mark.skip(reason="list should contain 'a'")
def test_should_contain_a(items):
    pass


@pytest.mark.skip(reason="list should not contain 'd'")
def test_should_not_contain_d(items):
    pass


@pytest.mark.skip(reason="list should contain 'c' and 'a'")
def test_should_contain_c_and_a(items):
    pass


@pytest.mark.skip(reason="list should not contain duplicates")
def test_should_not_contain_duplicates(items):
    pass


@pytest.mark.skip(reason="list should be precisely a, b, c ... but also loosely c, a, b")
def test_more(items):
    pass


@pytest.mark.skip(
    reason="map should have key 'k1', no key 'xxx', value 'v2', no value 'yyy', and item k2 => v2"
)
def test_map(mapping):
    pass
