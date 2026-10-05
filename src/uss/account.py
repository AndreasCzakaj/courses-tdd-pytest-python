from dataclasses import dataclass
from datetime import datetime
from typing import Literal

AccountStatus = Literal["new", "verified"]


@dataclass(frozen=True)
class Account:
    id: str
    username: str
    # format: "<salt>:<hash>", see password.py
    password_hash: str
    email: str
    tc_accepted: datetime
    status: AccountStatus


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


@dataclass(frozen=True)
class UserSession:
    account_id: str
    username: str
    email: str
