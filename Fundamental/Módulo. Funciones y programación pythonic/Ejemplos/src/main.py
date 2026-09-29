from contextlib import contextmanager

# 1. Funciones


def greet():
    return "Hello, World!"


greet()


# Función con parámetros


def greet_user(name):
    print(f"Hello, {name}!")


greet_user("Fernando")


# Función que retorna un valor


def add(a, b):
    return a + b


result = add(10, 5)

print("Resultado:", result)


# 2. Argumentos posicionales


def introduce(name, age):
    print(f"Name: {name}")
    print(f"Age: {age}")


introduce("Fernando", 27)


# 3. Argumentos nombrados

introduce(age=27, name="Fernando")


# 4. Argumentos con valores por defecto


def greet_with_default(name="User"):
    print(f"Hello, {name}!")


greet_with_default()

greet_with_default("Fernando")


# 5. *args


def add_numbers(*args):
    total = 0

    for number in args:
        total += number

    return total


print("Suma:", add_numbers(1, 2))

print("Suma:", add_numbers(1, 2, 3, 4, 5))


# *args es una tupla


def show_args(*args):
    print("Argumentos:", args)
    print("Tipo:", type(args))


show_args(10, 20, 30)


# 6. **kwargs


def show_user(**kwargs):
    print("Usuario:", kwargs)
    print("Tipo:", type(kwargs))


show_user(name="Fernando", age=27, city="Mexico")


# 7. *args y **kwargs juntos


def show_data(*args, **kwargs):
    print("Argumentos:", args)
    print("Argumentos nombrados:", kwargs)


show_data(10, 20, 30, name="Fernando", age=27)


# 8. Desempaquetado con *


def add_three_numbers(a, b, c):
    return a + b + c


numbers = [10, 20, 30]

result = add_three_numbers(*numbers)

print("Resultado:", result)


# 9. Desempaquetado con **


def introduce_user(name, age):
    print(f"Name: {name}")
    print(f"Age: {age}")


user = {"name": "Fernando", "age": 27}

introduce_user(**user)


# 10. Lambdas

add_lambda = lambda a, b: a + b  # noqa: E731

print("Resultado lambda:", add_lambda(10, 5))


# Lambda con sorted()

users = [
    {"name": "Fernando", "age": 27},
    {"name": "Ana", "age": 20},
    {"name": "Luis", "age": 30},
]


users_sorted = sorted(users, key=lambda user: user["age"])


print("Usuarios ordenados:")

for user in users_sorted:
    print(user)


# 11. Closures


def create_multiplier(number):
    def multiplier(value):
        return value * number

    return multiplier


double = create_multiplier(2)

triple = create_multiplier(3)


print("Double:", double(10))

print("Triple:", triple(10))


# 12. Decoradores


def logger(function):
    def wrapper():
        print("Function started")

        function()

        print("Function finished")

    return wrapper


@logger
def say_hello():
    print("Hello, World!")


say_hello()


# Decorador con argumentos


def logger_with_arguments(function):
    def wrapper(*args, **kwargs):
        print("Function started")

        result = function(*args, **kwargs)

        print("Function finished")

        return result

    return wrapper


@logger_with_arguments
def multiply(a, b):
    return a * b


result = multiply(10, 5)

print("Resultado:", result)


# 13. Iteradores

numbers = [10, 20, 30]

iterator = iter(numbers)


print("Primer elemento:", next(iterator))

print("Segundo elemento:", next(iterator))

print("Tercer elemento:", next(iterator))


# Iterador usando for

for number in numbers:
    print("Número:", number)


# 14. Crear un iterador


class Counter:
    def __init__(self, max_value):
        self.current = 0
        self.max_value = max_value

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max_value:
            raise StopIteration

        self.current += 1

        return self.current


counter = Counter(3)


for number in counter:
    print("Counter:", number)


# 15. Generadores


def generate_numbers():
    yield 1
    yield 2
    yield 3


for number in generate_numbers():
    print("Generator:", number)


# 16. Generador dinámico


def count(max_value):
    number = 1

    while number <= max_value:
        yield number

        number += 1


for number in count(5):
    print("Count:", number)


# 17. Generador infinito


def infinite_numbers():
    number = 0

    while True:
        yield number

        number += 1


numbers_generator = infinite_numbers()


print("Infinite:", next(numbers_generator))

print("Infinite:", next(numbers_generator))

print("Infinite:", next(numbers_generator))


# 18. Comprensión de listas

numbers = [1, 2, 3, 4, 5]


squares = [number**2 for number in numbers]


print("Cuadrados:", squares)


# 19. Comprensión de listas con condición

numbers = [1, 2, 3, 4, 5, 6]


even_numbers = [number for number in numbers if number % 2 == 0]


print("Números pares:", even_numbers)


# 20. Comprensión de diccionarios

numbers = [1, 2, 3, 4, 5]


squares_dict = {number: number**2 for number in numbers}


print("Diccionario:", squares_dict)


# 21. Comprensión de sets

numbers = [1, 2, 2, 3, 3, 4]


unique_numbers = {number for number in numbers}


print("Números únicos:", unique_numbers)


# 22. Context Manager con with

with open("data.txt", "w", encoding="utf-8") as file:
    file.write("Hello from Python")


# Leer el archivo usando with

with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()


print("Contenido:", content)


# 23. with + manejo de errores

try:
    with open("data.txt", "r", encoding="utf-8") as file:
        content = file.read()

    print("Archivo leído correctamente")

except FileNotFoundError:
    print("No se encontró el archivo")


# 24. Crear nuestro propio Context Manager


class DatabaseConnection:
    def __enter__(self):
        print("Opening connection")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing connection")


with DatabaseConnection():
    print("Executing query")


# 25. Context Manager con contextlib


@contextmanager
def connection():
    print("Opening connection")

    try:
        yield

    finally:
        print("Closing connection")


with connection():
    print("Executing query")
