import json
from pathlib import Path

from matchers.person import Person

PPL_JSON = Path(__file__).parent / "ppl.json"


class First:
    def __init__(self):
        self.map = {"k1": "v1", "k2": "v2"}

    def get_email(self) -> str:
        return "andreas.czakaj@binary-stars.eu"

    def get_list(self) -> list[str]:
        return ["a", "b", "c"]

    def get_people(self) -> list[Person]:
        with open(PPL_JSON, encoding="utf-8") as file:
            return [
                Person(
                    id=item["id"],
                    first_name=item["firstName"],
                    last_name=item["lastName"],
                    email=item["email"],
                    ip_address=item["ipAddress"],
                )
                for item in json.load(file)
            ]

    def get_person(self) -> Person:
        raise ValueError("oops")
