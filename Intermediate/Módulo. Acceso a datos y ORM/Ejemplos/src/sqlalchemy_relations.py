from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)

DATABASE_URL = "sqlite:///relations.db"


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

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
    )

    content: Mapped[str] = mapped_column(
        String(500),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )

    user: Mapped[User] = relationship(
        back_populates="posts",
    )


engine = create_engine(
    DATABASE_URL,
)


def create_database() -> None:
    Base.metadata.create_all(engine)


def create_user_with_posts() -> None:
    with Session(engine) as session:
        user = User(
            name="Fernando",
        )

        user.posts = [
            Post(
                title="Introducción a Python",
                content="Aprendiendo Python.",
            ),
            Post(
                title="SQLAlchemy",
                content="Aprendiendo ORM.",
            ),
        ]

        session.add(user)
        session.commit()


def get_users() -> list[User]:
    with Session(engine) as session:
        statement = select(User).options(selectinload(User.posts))

        return list(session.scalars(statement))


def show_users_and_posts() -> None:
    users = get_users()

    for user in users:
        print(f"\nUsuario: {user.name}")

        for post in user.posts:
            print(f"  Post: {post.title}")


def main() -> None:
    print("SQLAlchemy - Relaciones")

    create_database()
    create_user_with_posts()

    show_users_and_posts()


if __name__ == "__main__":
    main()
