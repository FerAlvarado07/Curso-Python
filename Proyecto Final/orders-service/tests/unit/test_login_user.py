from uuid import UUID

import pytest

from src.application.use_cases.login_user import (
    InvalidCredentialsError,
    LoginUserUseCase,
)
from src.application.use_cases.register_user import RegisterUserUseCase
from tests.unit.test_register_user import FakeUserRepository


def test_login_with_valid_credentials():
    repository = FakeUserRepository()

    RegisterUserUseCase(repository).execute(
        "user@example.com",
        "StrongPassword123",
    )

    user = LoginUserUseCase(repository).execute(
        "user@example.com",
        "StrongPassword123",
    )

    assert user.email == "user@example.com"
    assert isinstance(user.id, UUID)


def test_login_rejects_invalid_password():
    repository = FakeUserRepository()

    RegisterUserUseCase(repository).execute(
        "user@example.com",
        "StrongPassword123",
    )

    with pytest.raises(InvalidCredentialsError):
        LoginUserUseCase(repository).execute(
            "user@example.com",
            "WrongPassword123",
        )


def test_login_rejects_unknown_email():
    repository = FakeUserRepository()

    with pytest.raises(InvalidCredentialsError):
        LoginUserUseCase(repository).execute(
            "unknown@example.com",
            "StrongPassword123",
        )
