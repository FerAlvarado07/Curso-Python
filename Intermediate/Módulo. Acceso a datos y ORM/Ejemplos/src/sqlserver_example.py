import pyodbc

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=curso_python;"
    "UID=sa;"
    "PWD=passtest12345;"
    "TrustServerCertificate=yes;"
)


def create_table() -> None:
    with pyodbc.connect(CONNECTION_STRING) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            IF NOT EXISTS (
                SELECT *
                FROM sysobjects
                WHERE name = 'users'
                AND xtype = 'U'
            )
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL
            )
            """)

        connection.commit()


def create_user(
    name: str,
    email: str,
) -> None:
    with pyodbc.connect(CONNECTION_STRING) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (name, email)
            VALUES (?, ?)
            """,
            name,
            email,
        )

        connection.commit()


def get_users() -> list[tuple]:
    with pyodbc.connect(CONNECTION_STRING) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, email
            FROM users
            ORDER BY id
            """)

        return cursor.fetchall()


def main() -> None:
    print("SQL Server")

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    for user in get_users():
        print(user)


if __name__ == "__main__":
    main()
