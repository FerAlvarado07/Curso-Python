from src.schemas.user import UserCreate, UserUpdate
from src.services.auth_service import hash_password

users: list[dict] = []

_next_id = 1


def get_all_users() -> list[dict]:
    return users


def get_user_by_id(
    user_id: int,
) -> dict | None:
    for user in users:
        if user["id"] == user_id:
            return user

    return None


def get_user_by_email(
    email: str,
) -> dict | None:
    for user in users:
        if user["email"] == email:
            return user

    return None


def create_user(
    user_data: UserCreate,
) -> dict:
    global _next_id

    user = {
        "id": _next_id,
        "name": user_data.name,
        "email": str(user_data.email),
        "password_hash": hash_password(
            user_data.password,
        ),
    }

    users.append(user)

    _next_id += 1

    return user


def update_user(
    user_id: int,
    user_data: UserUpdate,
) -> dict | None:
    user = get_user_by_id(user_id)

    if user is None:
        return None

    user["name"] = user_data.name
    user["email"] = str(user_data.email)

    return user


def delete_user(
    user_id: int,
) -> bool:
    user = get_user_by_id(user_id)

    if user is None:
        return False

    users.remove(user)

    return True
