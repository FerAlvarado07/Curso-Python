# Type hints, tipado estático, PEP 8, PEP 20, pre-commit y CI

from typing import Literal, Protocol, TypedDict

# 1. Type hints y typing avanzado

# Define la base del sistema de anotaciones de tipos de Python.


def addNumbers(a: int, b: int) -> int:
    return a + b


# Union

# Permite indicar que un valor puede ser de diferentes tipos.


def process_union(value: int | str) -> str:
    return str(value)


# Actualmente se recomienda utilizar | en lugar de Union
# cuando se utiliza Python 3.10 o superior.


# Literal

# Permite indicar que solamente determinados valores son válidos.


def set_theme(theme: Literal["light", "dark"]):
    print(theme)


# TypedDict

# Permite definir la estructura esperada de un diccionario.


class User(TypedDict):
    name: str
    age: int


# Protocol

# Permite definir un contrato que otras clases pueden cumplir
# sin necesidad de heredar explícitamente de él.


class Printable(Protocol):
    def print(self) -> str: ...


class PrintableUser:
    def print(self) -> str:
        return "Usuario"


def show(value: Printable):
    print(value.print())


# 2. mypy y pyright

# Python utiliza tipado dinámico.

value = 10
value = "Hola"

# Python permite cambiar el tipo de una variable durante la ejecución.

# Herramientas como mypy y pyright realizan análisis estático
# del código y pueden detectar errores de tipos antes de ejecutar
# el programa.


# Mypy

# Instalación con Poetry:

# poetry add --group dev mypy

# Ejecutar:

# poetry run mypy src


# Ejemplo:


def add(a: int, b: int) -> int:
    return a + b


# Esta llamada es incorrecta según el type hint:
#
# result = add("10", 20)
#
# mypy puede detectar que "10" no es compatible con int.


# Pyright

# Límites del tipado dinámico

# Las anotaciones de tipos no cambian el comportamiento de Python.

# Esta llamada también es incorrecta según el type hint:
#
# add("10", 20)
#
# Python no bloquea automáticamente esta llamada.


# Los type hints sirven principalmente como información para:
#
# - IDEs
# - Linters
# - mypy
# - pyright
# - Desarrolladores
# - Documentación


# 3. PEP 8

# PEP 8 es la guía de estilo de Python.

# Define recomendaciones para:
#
# - Indentación
# - Nombres de variables
# - Nombres de funciones
# - Nombres de clases
# - Imports
# - Espacios
# - Longitud de líneas
# - Comentarios
# - Organización del código


# Ejemplo recomendado:


def calculate_total(price, quantity):
    return price * quantity


# Evitar:

# def calculate_total(price,quantity): return price*quantity


# 4. Ruff

# Ruff es una herramienta rápida para análisis estático
# y formato de código.

# Puede utilizarse para:
#
# - Detectar errores
# - Aplicar reglas de estilo
# - Corregir problemas automáticamente
# - Organizar imports
# - Formatear código


# 5. Black

# Black es un formateador automático para Python.

# Su objetivo es mantener un formato consistente
# en todo el proyecto.


# 6. isort

# isort organiza automáticamente los imports de Python.

# Ruff también puede encargarse de la organización de imports.


# 7. PEP 20 — The Zen of Python

# PEP 20 contiene principios de diseño de Python.

# "Beautiful is better than ugly."
# "Simple is better than complex."
# "Explicit is better than implicit."
# "Readability counts."


# Ejemplos de ejecución
#
# Colocamos las llamadas que producen salida dentro de este bloque
# para evitar que se ejecuten cuando pytest importe el módulo.


if __name__ == "__main__":
    print("Type hints:")

    print("Suma:", addNumbers(10, 20))

    print("\nUnion:")
    print(process_union(100))
    print(process_union("100"))

    print("\nLiteral:")
    set_theme("dark")

    print("\nTypedDict:")

    user: User = {
        "name": "Fernando",
        "age": 27,
    }

    print(user)

    print("\nProtocol:")
    show(PrintableUser())

    print("\nTipado dinámico:")

    result = add(10, 20)

    print("Resultado:", result)
