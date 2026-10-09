from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from main import app
from src.api.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
)
from src.application.use_cases.login_user import (
    InvalidCredentialsError,
)
from src.application.use_cases.register_user import (
    EmailAlreadyRegisteredError,
)
from src.domain.entities.user import User


class FakeRegisterUseCase:
    def execute(self, email: str, password: str) -> User:
        if email == "existing@example.com":
            raise EmailAlreadyRegisteredError()

        return User(
            id=uuid4(),
            email=email.strip().lower(),
            hashed_password="hashed-value",
            created_at=datetime.now(timezone.utc),
        )


class FakeLoginUseCase:
    def execute(self, email: str, password: str) -> User:
        if email != "user@example.com" or password != "StrongPassword123":
            raise InvalidCredentialsError()

        return User(
            id=uuid4(),
            email=email,
            hashed_password="hashed-value",
            created_at=datetime.now(timezone.utc),
        )


def setup_function():
    app.dependency_overrides[get_register_user_use_case] = lambda: FakeRegisterUseCase()
    app.dependency_overrides[get_login_user_use_case] = lambda: FakeLoginUseCase()


def teardown_function():
    app.dependency_overrides.clear()


def test_register_returns_expected_contract():
    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "email": "new@example.com",
                "password": "StrongPassword123",
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"id", "email", "created_at"}
    assert body["email"] == "new@example.com"


def test_login_returns_bearer_token():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "StrongPassword123",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]
    assert body["user"]["email"] == "user@example.com"


def test_login_rejects_invalid_credentials():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "WrongPassword123",
            },
        )

    assert response.status_code == 401


def test_register_rejects_invalid_email():
    with TestClient(app) as client:
        response = client.post(
            "/auth/register",
            json={
                "email": "invalid-email",
                "password": "StrongPassword123",
            },
        )

    assert response.status_code == 422
