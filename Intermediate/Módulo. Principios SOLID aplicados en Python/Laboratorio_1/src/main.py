from typing import Protocol


class UserRepository(Protocol):
    def save(self, username: str) -> None: ...

    def find_by_username(
        self,
        username: str,
    ) -> str | None: ...


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users: list[str] = []

    def save(self, username: str) -> None:
        self.users.append(username)

    def find_by_username(
        self,
        username: str,
    ) -> str | None:
        if username in self.users:
            return username

        return None


class SqlUserRepository:
    def __init__(self) -> None:
        self.database: list[str] = []

    def save(self, username: str) -> None:
        print(f"INSERT INTO users (username) VALUES ('{username}')")

        self.database.append(username)

    def find_by_username(
        self,
        username: str,
    ) -> str | None:
        print(f"SELECT username FROM users WHERE username = '{username}'")

        if username in self.database:
            return username

        return None


class UserService:
    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self.repository = repository

    def create_user(
        self,
        username: str,
    ) -> None:
        existing_user = self.repository.find_by_username(username)

        if existing_user is not None:
            raise ValueError("El usuario ya existe")

        self.repository.save(username)

    def get_user(
        self,
        username: str,
    ) -> str | None:
        return self.repository.find_by_username(username)


def verify_repository(
    repository: UserRepository,
) -> None:
    repository.save("Fernando")

    result = repository.find_by_username("Fernando")

    assert result == "Fernando"


def main() -> None:
    print("\n InMemoryUserRepository:")

    memory_repository = InMemoryUserRepository()

    memory_service = UserService(memory_repository)

    memory_service.create_user("Fernando")

    print(memory_service.get_user("Fernando"))

    print("\n SqlUserRepository:")

    sql_repository = SqlUserRepository()

    sql_service = UserService(sql_repository)

    sql_service.create_user("Fernando")

    print(sql_service.get_user("Fernando"))

    print("\n Verificación LSP:")

    verify_repository(memory_repository)

    verify_repository(sql_repository)

    print("\nLSP verificado correctamente")


if __name__ == "__main__":
    main()
