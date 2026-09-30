from typing import Literal, Protocol, TypedDict


def add_numbers(a: int, b: int) -> int:
    return a + b


def process(value: int | str) -> str:
    return str(value)


def set_theme(theme: Literal["light", "dark"]) -> str:
    return f"Tema seleccionado: {theme}"


class User(TypedDict):
    name: str
    age: int


def create_user(name: str, age: int) -> User:
    return {
        "name": name,
        "age": age,
    }


class Printable(Protocol):
    def print(self) -> str: ...


class UserPrinter:
    def __init__(self, name: str):
        self.name = name

    def print(self) -> str:
        return f"Usuario: {self.name}"


def show(value: Printable) -> None:
    print(value.print())


def calculate_total(price: float, quantity: int) -> float:
    return price * quantity


if __name__ == "__main__":
    print("Type hints:")
    print("Suma:", add_numbers(10, 20))

    print("\nUnion:")
    print(process(100))
    print(process("100"))

    print("\nLiteral:")
    print(set_theme("dark"))

    print("\nTypedDict:")
    user = create_user("Fernando", 27)
    print(user)

    print("\nProtocol:")
    show(UserPrinter("Fernando"))

    print("\nCálculo:")
    print("Total:", calculate_total(150.50, 3))
