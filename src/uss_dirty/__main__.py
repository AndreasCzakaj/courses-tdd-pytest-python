"""Starts the user self service for local use: `cd src`, then `python -m uss_dirty`.

The database is a temporary SQLite file, filled with the accounts below.
"""

import hashlib
import os
import secrets
import sqlite3
import tempfile
import uuid
from datetime import datetime, timezone

from uss_dirty.server import app

ACCOUNTS = [
    {"username": "alice_verified", "password": "Correct-Horse_42", "status": "verified"},
    {"username": "bob_not_verified", "password": "Battery.Staple+7", "status": "new"},
]


def hash_password(password: str) -> str:
    """format: "<salt>:<hash>", both hex encoded"""
    salt = secrets.token_hex(16)
    return salt + ":" + hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1, dklen=64).hex()


def create_database() -> str:
    db_path = os.path.join(tempfile.mkdtemp(prefix="uss-"), "uss.db")
    connection = sqlite3.connect(db_path)
    connection.execute(
        "CREATE TABLE accounts ("
        "id TEXT PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, email TEXT, tc_accepted TEXT, status TEXT)"
    )
    for account in ACCOUNTS:
        connection.execute(
            "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                account["username"],
                hash_password(account["password"]),
                account["username"] + "@example.com",
                datetime.now(timezone.utc).isoformat(),
                account["status"],
            ),
        )
    connection.commit()
    connection.close()
    return db_path


def main() -> None:
    db_path = create_database()
    os.environ["USS_DB"] = db_path

    print("SQLite database:", db_path)
    for account in ACCOUNTS:
        print(" ", account)

    app.run(port=int(os.environ.get("PORT", "3000")))


if __name__ == "__main__":
    main()
