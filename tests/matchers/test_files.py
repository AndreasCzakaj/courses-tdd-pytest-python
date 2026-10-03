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


def test_txt_file_should_exist_and_contain_first_and_second_line(new_file):
    assert new_file.exists()
    assert new_file.is_file()

    content = new_file.read_text(encoding="utf-8")
    assert "The first line" in content
    assert "The second line" in content
    assert content.splitlines() == ["The first line", "The second line"]


def test_other_file_should_not_exist(new_file):
    assert not (new_file.parent / "other_file.txt").exists()
    assert list(new_file.parent.iterdir()) == [new_file]


def test_json_file():
    assert PPL_JSON.exists()
    people = json.loads(PPL_JSON.read_text(encoding="utf-8"))

    assert isinstance(people, list)
    assert len(people) == 1000

    # JSON is parsed into lists and dicts, which are compared by value
    assert people[17] == {
        "id": 18,
        "firstName": "Crawford",
        "lastName": "Roisen",
        "email": "croisenh@independent.co.uk",
        "ipAddress": "163.170.23.182",
    }
