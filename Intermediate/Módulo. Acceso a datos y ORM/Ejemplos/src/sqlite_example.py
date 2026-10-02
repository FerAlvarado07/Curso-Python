import sqlite3
from pathlib import Path

DATABASE = Path("database.db")


def create_table() -> None:
    with sqlite3.connect(DATABASE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
            """)


def create_user(name: str, email: str) -> None:
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            """
            INSERT INTO users (name, email)
            VALUES (?, ?)
            """,
            (name, email),
        )


def get_users() -> list[tuple]:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.execute("""
            SELECT id, name, email
            FROM users
            ORDER BY id
            """)

        return cursor.fetchall()


def get_user(user_id: int) -> tuple | None:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )

        return cursor.fetchone()


def update_user(
    user_id: int,
    name: str,
) -> None:
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            """
            UPDATE users
            SET name = ?
            WHERE id = ?
            """,
            (name, user_id),
        )


def delete_user(user_id: int) -> None:
    with sqlite3.connect(DATABASE) as connection:
        connection.execute(
            """
            DELETE FROM users
            WHERE id = ?
            """,
            (user_id,),
        )


def main() -> None:
    print("SQLite")

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    create_user(
        "Ana",
        "ana@example.com",
    )

    print("\nUsuarios:")

    for user in get_users():
        print(user)

    print("\nUsuario con ID 1:")
    print(get_user(1))

    update_user(
        1,
        "Fernando Enrique",
    )

    print("\nDespués de actualizar:")
    print(get_user(1))

    delete_user(2)

    print("\nDespués de eliminar:")
    print(get_users())


if __name__ == "__main__":
    main()
