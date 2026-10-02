from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.sqlalchemy_orm_example import (
    Base,
    User,
)


def create_user(
    session: Session,
    name: str,
    email: str,
) -> User:
    user = User(
        name=name,
        email=email,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user(
    session: Session,
    user_id: int,
) -> User | None:
    return session.get(
        User,
        user_id,
    )


def test_create_and_get_user():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = create_user(
            session,
            "Fernando",
            "fernando@example.com",
        )

        result = get_user(
            session,
            user.id,
        )

        assert result is not None
        assert result.name == "Fernando"
        assert result.email == "fernando@example.com"


def test_get_user_not_found():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        result = get_user(
            session,
            999,
        )

        assert result is None
