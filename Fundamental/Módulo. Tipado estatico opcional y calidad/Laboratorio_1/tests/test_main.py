from src.main import (
    UserPrinter,
    add_numbers,
    calculate_total,
    create_user,
    process,
    set_theme,
    show,
)


def test_add_numbers():
    assert add_numbers(10, 20) == 30


def test_process():
    assert process(100) == "100"
    assert process("100") == "100"


def test_set_theme():
    assert set_theme("dark") == "Tema seleccionado: dark"


def test_create_user():
    user = create_user("Fernando", 27)

    assert user["name"] == "Fernando"
    assert user["age"] == 27


def test_calculate_total():
    assert calculate_total(150.50, 3) == 451.50


def test_protocol(capsys):
    show(UserPrinter("Fernando"))

    captured = capsys.readouterr()

    assert captured.out == "Usuario: Fernando\n"
