"""Starts the user self service for local use: `cd src`, then `python -m uss`.

The database is a temporary SQLite file, filled with the accounts below.
"""

import os
import tempfile
import uuid
from datetime import datetime, timezone

from uss.account import Account
from uss.account_dao_sqlite_impl import AccountDaoSqliteImpl
from uss.password import hash_password
from uss.server import create_app

ACCOUNTS = [
    {"username": "alice_verified", "password": "Correct-Horse_42", "status": "verified"},
    {"username": "bob_not_verified", "password": "Battery.Staple+7", "status": "new"},
]


def create_database() -> str:
    db_path = os.path.join(tempfile.mkdtemp(prefix="uss-"), "uss.db")
    account_dao = AccountDaoSqliteImpl(db_path)
    account_dao.create_table()
    for account in ACCOUNTS:
        account_dao.save(
            Account(
                id=str(uuid.uuid4()),
                username=account["username"],
                password_hash=hash_password(account["password"]),
                email=account["username"] + "@example.com",
                tc_accepted=datetime.now(timezone.utc),
                status=account["status"],
            )
        )
    return db_path


def main() -> None:
    db_path = create_database()

    print("SQLite database:", db_path)
    for account in ACCOUNTS:
        print(" ", account)

    create_app(db_path).run(port=int(os.environ.get("PORT", "3000")))


if __name__ == "__main__":
    main()
