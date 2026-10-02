import psycopg

DATABASE_URL = "postgresql://postgres:password@localhost:5432/curso_python"


def create_table() -> None:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(150) UNIQUE NOT NULL
                )
                """)


def create_user(
    name: str,
    email: str,
) -> None:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (name, email)
                VALUES (%s, %s)
                """,
                (name, email),
            )


def get_users() -> list[tuple]:
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, email
                FROM users
                ORDER BY id
                """)

            return cursor.fetchall()


def main() -> None:
    print("PostgreSQL")

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    for user in get_users():
        print(user)


if __name__ == "__main__":
    main()
