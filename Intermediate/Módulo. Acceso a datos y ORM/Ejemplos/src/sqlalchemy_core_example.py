from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    insert,
    select,
)

DATABASE_URL = "sqlite:///core.db"

engine = create_engine(
    DATABASE_URL,
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "name",
        String(100),
        nullable=False,
    ),
    Column(
        "email",
        String(150),
        nullable=False,
        unique=True,
    ),
)


def create_table() -> None:
    metadata.create_all(engine)


def create_user(
    name: str,
    email: str,
) -> None:
    statement = insert(users).values(
        name=name,
        email=email,
    )

    with engine.begin() as connection:
        connection.execute(statement)


def get_users() -> list:
    statement = select(users)

    with engine.connect() as connection:
        result = connection.execute(statement)

        return result.fetchall()


def main() -> None:
    print("SQLAlchemy Core")

    create_table()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    for user in get_users():
        print(user)


if __name__ == "__main__":
    main()
