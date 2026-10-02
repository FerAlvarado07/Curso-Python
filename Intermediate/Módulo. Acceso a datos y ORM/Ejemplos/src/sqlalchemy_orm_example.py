from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)

DATABASE_URL = "sqlite:///orm.db"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


engine = create_engine(
    DATABASE_URL,
)


def create_database() -> None:
    Base.metadata.create_all(engine)


def create_user(
    name: str,
    email: str,
) -> None:
    with Session(engine) as session:
        user = User(
            name=name,
            email=email,
        )

        session.add(user)
        session.commit()


def get_users() -> list[User]:
    with Session(engine) as session:
        statement = select(User)

        return list(session.scalars(statement))


def get_user(
    user_id: int,
) -> User | None:
    with Session(engine) as session:
        return session.get(
            User,
            user_id,
        )


def update_user(
    user_id: int,
    name: str,
) -> None:
    with Session(engine) as session:
        user = session.get(
            User,
            user_id,
        )

        if user:
            user.name = name
            session.commit()


def delete_user(
    user_id: int,
) -> None:
    with Session(engine) as session:
        user = session.get(
            User,
            user_id,
        )

        if user:
            session.delete(user)
            session.commit()


def main() -> None:
    print("SQLAlchemy ORM")

    create_database()

    create_user(
        "Fernando",
        "fernando@example.com",
    )

    print("\nUsuarios:")

    for user in get_users():
        print(user)

    print("\nBuscar usuario:")
    print(get_user(1))

    update_user(
        1,
        "Fernando Enrique",
    )

    print("\nDespués de actualizar:")
    print(get_user(1))

    delete_user(1)

    print("\nDespués de eliminar:")
    print(get_users())


if __name__ == "__main__":
    main()
