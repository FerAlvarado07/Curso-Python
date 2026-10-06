from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.services.auth_service import hash_password


def get_all_users(session: Session) -> list[User]:
    statement = select(User).order_by(User.id)

    return list(session.scalars(statement))


def get_user_by_id(
    session: Session,
    user_id: int,
) -> User | None:
    return session.get(
        User,
        user_id,
    )


def get_user_by_email(
    session: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return session.scalars(statement).first()


def create_user(
    session: Session,
    user_data: UserCreate,
) -> User:
    user = User(
        name=user_data.name,
        email=str(user_data.email),
        password_hash=hash_password(
            user_data.password,
        ),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def update_user(
    session: Session,
    user: User,
    user_data: UserUpdate,
) -> User:
    user.name = user_data.name
    user.email = str(user_data.email)

    session.commit()
    session.refresh(user)

    return user


def delete_user(
    session: Session,
    user: User,
) -> None:
    session.delete(user)
    session.commit()
