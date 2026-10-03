from operator import attrgetter

import pytest
from pytest_check import check

from matchers.first import First
from matchers.person import Person


@pytest.fixture
def first() -> First:
    return First()


@pytest.fixture
def people(first) -> list[Person]:
    return first.get_people()


@pytest.fixture
def first_person(people) -> Person:
    return people[0]


def test_people_should_contain_1000_people(people):
    assert len(people) == 1000


def test_first_person(first_person):
    expected = Person(
        id=1,
        first_name="Skippy",
        last_name="Rayne",
        email="srayne0@dot.gov",
        ip_address="229.183.132.150",
    )

    assert first_person.id == expected.id
    assert first_person.first_name == expected.first_name
    assert first_person.last_name == expected.last_name
    assert first_person.email == expected.email
    assert first_person.ip_address == expected.ip_address

    # alternative: soft assertions
    with check:
        assert first_person.id == expected.id
    with check:
        assert first_person.first_name == expected.first_name
    with check:
        assert first_person.last_name == expected.last_name
    with check:
        assert first_person.email == expected.email
    with check:
        assert first_person.ip_address == expected.ip_address

    # batch!
    assert vars(first_person) == vars(expected)


def test_first_person_in_one_go(first_person):
    expected = Person(
        id=1,
        first_name="Skippy",
        last_name="Rayne",
        email="srayne0@dot.gov",
        ip_address="229.183.132.150",
    )

    # `Person` does not implement `__eq__`, so `==` compares identity
    assert first_person != expected

    # `vars(...)` yields the fields as dict, and dicts are compared by value
    assert vars(first_person) == vars(expected)

    # Tip: a `@dataclass` generates `__eq__` for you => `first_person == expected`


def test_first_person_partially(first_person):
    expected = Person(id=1, first_name="Skippy", last_name="Rayne")

    # variant 1: selected fields
    selected = attrgetter("id", "first_name", "last_name")
    assert selected(first_person) == selected(expected)

    # variant 2: subtracted fields
    ignored = {"email", "ip_address"}
    assert {k: v for k, v in vars(first_person).items() if k not in ignored} == {
        k: v for k, v in vars(expected).items() if k not in ignored
    }

    # variant 3: compact
    assert (first_person.id, first_person.first_name, first_person.last_name) == (1, "Skippy", "Rayne")

    # variant 4: "is superset of"
    assert vars(first_person).items() >= {"id": 1, "first_name": "Skippy", "last_name": "Rayne"}.items()


def test_get_person_raises_error(first):
    # variant 1
    with pytest.raises(ValueError) as error:
        first.get_person()
    assert type(error.value) is ValueError
    assert str(error.value) == "oops"

    # variant 2: `match` is a regular expression (search)
    with pytest.raises(ValueError, match="^oops$"):
        first.get_person()
