import sqlite3

from src.sqlite_example import (
    create_table,
    create_user,
    get_user,
    get_users,
    update_user,
)


def test_create_table(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.sqlite_example.DATABASE",
        database,
    )

    create_table()

    with sqlite3.connect(database) as connection:
        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'users'
            """)

        result = cursor.fetchone()

    assert result == ("users",)


def test_create_user(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.sqlite_example.DATABASE",
        database,
    )

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    user = get_user(1)

    assert user is not None
    assert user[1] == "Fernando"
    assert user[2] == "fernando@example.com"


def test_get_users(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.sqlite_example.DATABASE",
        database,
    )

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    create_user(
        "Ana",
        "ana@example.com",
    )

    users = get_users()

    assert len(users) == 2
    assert users[0][1] == "Fernando"
    assert users[1][1] == "Ana"


def test_update_user(tmp_path, monkeypatch):
    database = tmp_path / "test.db"

    monkeypatch.setattr(
        "src.sqlite_example.DATABASE",
        database,
    )

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    update_user(
        1,
        "Fernando Enrique",
    )

    user = get_user(1)

    assert user is not None
    assert user[1] == "Fernando Enrique"
