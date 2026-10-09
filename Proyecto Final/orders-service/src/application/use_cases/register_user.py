from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.security.password_service import hash_password


class EmailAlreadyRegisteredError(Exception):
    pass


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, email: str, password: str) -> User:
        normalized_email = email.strip().lower()

        if self._repository.find_by_email(normalized_email):
            raise EmailAlreadyRegisteredError

        user = User(
            id=uuid4(),
            email=normalized_email,
            hashed_password=hash_password(password),
            created_at=datetime.now(timezone.utc),
        )

        return self._repository.save(user)
