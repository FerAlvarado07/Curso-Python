from uuid import UUID

import pytest

from src.application.use_cases.register_user import (
    EmailAlreadyRegisteredError,
    RegisterUserUseCase,
)
from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository


class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> User:
        self.users[user.email] = user
        return user

    def find_by_email(self, email: str) -> User | None:
        return self.users.get(email)

    def find_by_id(self, user_id: UUID) -> User | None:
        return next(
            (user for user in self.users.values() if user.id == user_id),
            None,
        )


def test_register_user_successfully():
    repository = FakeUserRepository()
    use_case = RegisterUserUseCase(repository)

    user = use_case.execute(
        "USER@example.com",
        "StrongPassword123",
    )

    assert user.email == "user@example.com"
    assert user.hashed_password != "StrongPassword123"
    assert repository.find_by_email(user.email) is not None


def test_register_user_rejects_duplicate_email():
    repository = FakeUserRepository()
    use_case = RegisterUserUseCase(repository)

    use_case.execute("user@example.com", "StrongPassword123")

    with pytest.raises(EmailAlreadyRegisteredError):
        use_case.execute("user@example.com", "AnotherPassword123")
