import json
from pathlib import Path

import pytest

from matchers.first import PPL_JSON


@pytest.fixture
def new_file(tmp_path: Path) -> Path:
    # `tmp_path` is a built-in fixture: a fresh temp dir per test
    assert tmp_path.is_dir()
    file = tmp_path / "new_file.txt"
    assert not file.exists()

    file.write_text("The first line\nThe second line\n", encoding="utf-8")
    return file


@pytest.mark.skip(reason="new_file should exist and contain the first and second line")
def test_txt_file_should_exist_and_contain_first_and_second_line(new_file):
    # "The first line"
    # "The second line"
    pass


@pytest.mark.skip(reason="some other file in the same folder should not exist")
def test_other_file_should_not_exist(new_file):
    pass


def test_json_file():
    assert PPL_JSON.exists()
    people = json.loads(PPL_JSON.read_text(encoding="utf-8"))

    assert isinstance(people, list)
    assert len(people) == 1000
