import pytest

from src.main import (
    InMemoryUserRepository,
    SqlUserRepository,
    UserService,
    verify_repository,
)


def test_create_user() -> None:
    repository = InMemoryUserRepository()
    service = UserService(repository)

    service.create_user("Fernando")

    assert service.get_user("Fernando") == "Fernando"


def test_user_cannot_be_created_twice() -> None:
    repository = InMemoryUserRepository()
    service = UserService(repository)

    service.create_user("Fernando")

    with pytest.raises(ValueError):
        service.create_user("Fernando")


def test_sql_repository() -> None:
    repository = SqlUserRepository()
    service = UserService(repository)

    service.create_user("Fernando")

    assert service.get_user("Fernando") == "Fernando"


def test_lsp_with_memory_repository() -> None:
    repository = InMemoryUserRepository()

    verify_repository(repository)


def test_lsp_with_sql_repository() -> None:
    repository = SqlUserRepository()

    verify_repository(repository)
