import pytest

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


@pytest.mark.skip(reason="people should contain 1000 people")
def test_people_should_contain_1000_people(people):
    pass


@pytest.mark.skip(reason="first person should have the expected values, field by field")
def test_first_person(first_person):
    expected = Person(
        id=1,
        first_name="Skippy",
        last_name="Rayne",
        email="srayne0@dot.gov",
        ip_address="229.183.132.150",
    )


@pytest.mark.skip(reason="first person should equal the expected person, in one go")
def test_first_person_in_one_go(first_person):
    expected = Person(
        id=1,
        first_name="Skippy",
        last_name="Rayne",
        email="srayne0@dot.gov",
        ip_address="229.183.132.150",
    )


@pytest.mark.skip(reason="first person should match id, first_name and last_name only")
def test_first_person_partially(first_person):
    expected = Person(id=1, first_name="Skippy", last_name="Rayne")


@pytest.mark.skip(reason="get_person should raise a ValueError with message 'oops' (2 variants)")
def test_get_person_raises_error(first):
    pass
