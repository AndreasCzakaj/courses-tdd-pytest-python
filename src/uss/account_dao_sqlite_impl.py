import sqlite3
from contextlib import closing
from datetime import datetime

from uss.account import Account
from uss.account_dao import AccountDao, DaoError

CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS accounts (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        email TEXT,
        tc_accepted TEXT,
        status TEXT
    )
"""
INSERT = "INSERT INTO accounts (id, username, password_hash, email, tc_accepted, status) VALUES (?, ?, ?, ?, ?, ?)"
SELECT_BY_USERNAME = "SELECT id, username, password_hash, email, tc_accepted, status FROM accounts WHERE username = ?"


class AccountDaoSqliteImpl(AccountDao):
    def __init__(self, db_path: str):
        self._db_path = db_path

    def create_table(self) -> None:
        self._execute(CREATE_TABLE)

    def save(self, account: Account) -> None:
        self._execute(
            INSERT,
            (
                account.id,
                account.username,
                account.password_hash,
                account.email,
                account.tc_accepted.isoformat(),
                account.status,
            ),
        )

    def find_by_username(self, username: str) -> Account | None:
        rows = self._execute(SELECT_BY_USERNAME, (username,))
        return _to_account(rows[0]) if rows else None

    def _execute(self, sql: str, params: tuple = ()) -> list[tuple]:
        try:
            # `closing` closes the connection, `with connection` commits
            with closing(sqlite3.connect(self._db_path)) as connection, connection:
                return connection.execute(sql, params).fetchall()
        except sqlite3.Error as e:
            raise DaoError("SQLite Error") from e


def _to_account(row: tuple) -> Account:
    id, username, password_hash, email, tc_accepted, status = row
    return Account(
        id=id,
        username=username,
        password_hash=password_hash,
        email=email,
        tc_accepted=datetime.fromisoformat(tc_accepted),
        status=status,
    )
