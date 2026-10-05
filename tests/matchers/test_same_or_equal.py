"""Same or equal? No exercise, but an illustration: all tests are GREEN.

- `is` checks IDENTITY: the very same instance
- `==` checks EQUALITY: it calls `__eq__`, so the class decides what "equal" means
"""

from dataclasses import dataclass

from matchers.person import Person


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Pixel:
    x: int
    y: int


def test_lists_with_the_same_items_are_equal_but_not_same():
    numbers = [1, 2, 3]
    other_numbers = [1, 2, 3]

    assert numbers == other_numbers
    assert numbers is not other_numbers


def test_an_object_is_only_the_same_as_itself():
    numbers = [1, 2, 3]
    also_numbers = numbers

    # 2 variables, 1 instance
    assert also_numbers is numbers

    # a copy is a new instance
    assert numbers.copy() is not numbers
    assert numbers.copy() == numbers


def test_numbers_of_different_types_are_equal():
    # `==` does not check the type ...
    assert 42 == 42.0
    assert 1 == True  # noqa: E712

    # ... so check it yourself if it matters
    assert type(42) is not type(42.0)


def test_a_number_and_a_string_are_never_equal():
    # no implicit conversion, unlike PHP or JavaScript
    assert 42 != "42"


def test_none_is_checked_by_identity():
    nothing = None

    # there is only 1 `None` => `is`, not `==`
    assert nothing is None


def test_objects_without_eq_are_only_equal_to_themselves():
    kim = Person(id=24, first_name="Kim")
    other_kim = Person(id=24, first_name="Kim")

    # `Person` does not implement `__eq__` => `==` falls back to identity
    assert kim != other_kim
    assert kim is not other_kim

    # `vars(...)` yields the fields as dict, and dicts are compared by value
    assert vars(kim) == vars(other_kim)


def test_dataclasses_with_the_same_values_are_equal_but_not_same():
    # a `@dataclass` generates `__eq__`: same class, same values
    assert Point(1, 2) == Point(1, 2)
    assert Point(1, 2) is not Point(1, 2)

    assert Point(1, 2) != Point(1, 3)


def test_dataclasses_of_different_classes_are_not_equal():
    # same fields, same values ...
    assert vars(Point(1, 2)) == vars(Pixel(1, 2))

    # ... but another class
    assert Point(1, 2) != Pixel(1, 2)
