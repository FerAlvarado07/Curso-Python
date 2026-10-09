import os
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.user import User
from src.infrastructure.database.models import Base
from src.infrastructure.database.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


@pytest.fixture
def session():
    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")

    engine = create_engine(database_url, pool_pre_ping=True)

    # Requiere una base de datos desechable, exclusiva para pruebas.
    Base.metadata.create_all(engine)

    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    db_session = TestingSession()

    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_user_repository_persists_and_finds_user(session):
    repository = SqlAlchemyUserRepository(session)

    user = User(
        id=uuid4(),
        email="integration@example.com",
        hashed_password="test-hash",
        created_at=datetime.now(timezone.utc),
    )

    repository.save(user)

    result = repository.find_by_email("integration@example.com")

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email
    assert result.hashed_password == "test-hash"
