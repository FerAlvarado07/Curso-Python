import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.database import get_session
from src.main import app
from src.models import Base
from src.models.user import User
from src.services.auth_service import hash_password


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client, db_session):
    user = User(
        name="Fernando",
        email="fernando@axity.com",
        password_hash=hash_password("12345678"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    login_response = client.post(
        "/auth/login",
        data={
            "username": user.email,
            "password": "12345678",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["data"]["access_token"]

    client.headers.update(
        {
            "Authorization": f"Bearer {token}",
        }
    )

    return client
