from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.security.password_service import verify_password


class InvalidCredentialsError(Exception):
    pass


class LoginUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, email: str, password: str) -> User:
        normalized_email = email.strip().lower()
        user = self._repository.find_by_email(normalized_email)

        if user is None or not verify_password(
            password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError

        return user
