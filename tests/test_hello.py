import pytest

from hello import Hello


@pytest.fixture
def sut() -> Hello:
    return Hello()


def test_it_should_yield_42_for_the_ultimate_question(sut):
    # given
    question = "What is the answer to the Ultimate Question of Life, the Universe, and Everything?"

    # when
    actual = sut.answer(question)

    # then
    assert actual == 42, "it should be as Douglas Adams said"
