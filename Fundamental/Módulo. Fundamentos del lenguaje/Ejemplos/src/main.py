import re

# Sintaxis, indentación, variables y alcance


def toGreet():
    return "Hello, World!"


if __name__ == "__main__":
    # ############## INDENTACIÓN #############

    name = "Fernando"
    age = 27

    print(name)
    print(age)

    # #########################

    age = 27

    if age >= 18:
        print("Es mayor de edad")

    # #########################

    age = 27

    if age >= 18:
        print("Es mayor de edad")
        print("Puede votar")

    # #########################

    def Greet():
        print("Hello")
        print("Welcome")

    Greet()

    # ############## VARIABLES #############

    name = "Fernando"
    age = 25
    salary = 15000.50
    active = True

    print(type(age))

    # ############## COLECCIONES #############

    print("Listas:")

    fruits = ["apple", "pear", "orange"]

    print(fruits)

    print(fruits[0])
    print(fruits[1])

    fruits[0] = "banana"

    fruits.append("grape")

    print(fruits)

    print("Tuplas:")

    colors = ("red", "green", "blue")

    print(colors)

    print(colors[0])
    print(colors[1])

    print("Diccionarios:")

    person = {"name": "Fernando", "age": 27, "city": "Madrid"}

    print(person)

    print(person["name"])
    print(person["age"])

    person["age"] = 28

    print(person)

    print("Sets:")

    numbers = {1, 2, 3, 3, 4, 4}

    print(numbers)

    numbers.add(5)
    numbers.remove(2)

    # ############## SCOPE #############

    name_global = "Fernando"

    def GreetGlobal():
        print(name_global)

    GreetGlobal()

    # #############################

    def GreetLocal():
        MESSAGE = "Hello Fernando"
        print(MESSAGE)

    GreetLocal()

    # ############## CONTROLES DE FLUJO #############

    # if

    age = 25

    if age >= 18:
        print("Es mayor de edad")

    # if-else

    age = 15

    if age >= 18:
        print("Es mayor de edad")
    else:
        print("Es menor de edad")

    # if-elif-else

    grade = 85

    if grade >= 90:
        print("Excelente")
    elif grade >= 70:
        print("Aprobado")
    else:
        print("No aprobado")

    # Switch/Match

    option = 2

    match option:
        case 1:
            print("Home")
        case 2:
            print("Profile")
        case 3:
            print("Settings")
        case _:
            print("Unknown option")

    # For loop

    fruits = ["apple", "pear", "orange"]

    for fruit in fruits:
        print(fruit)

    # Range

    for number in range(1, 6):
        print(number)

    # While loop

    counter = 0

    while counter < 5:
        print(counter)
        counter += 1

    # ############## PATTERN MATCHING #############

    user = {"name": "Fernando", "age": 25}

    match user:
        case {"name": name, "age": age}:
            print(f"{name} tiene {age} años")

    # ############## EXPRESIONES REGULARES #############

    text = "Mi edad es 25"

    result = re.search(r"\d+", text)

    print(result.group())

    # ####

    text = "cat"

    result = re.search(r"c.t", text)

    print(result.group())

    # ####

    text = "ABC123"

    result = re.findall(r"\D+", text)

    print(result)

    # ############## MANEJO DE EXCEPCIONES #############

    try:
        number = int("hello")
    except ValueError:
        print("Debes ingresar un número válido")

    # Varias excepciones

    try:
        number = int(input("Ingrese un número: "))
        result = 10 / number

        print(result)

    except ValueError:
        print("Debes ingresar un número válido")

    except ZeroDivisionError:
        print("No puedes ingresar cero")

    # else en manejo de excepciones

    try:
        number = int("10")

    except ValueError:
        print("Valor inválido")

    else:
        print("Código ejecutado correctamente")

    # finally en manejo de excepciones

    try:
        number = int("10")

    except ValueError:
        print("Valor inválido")

    finally:
        print("Proceso finalizado")

    # ############### EJEMPLO CONJUNTO #############

    users = [
        {"name": "Fernando", "age": 27},
        {"name": "Ana", "age": 17},
        {"name": "Luis", "age": 30},
    ]

    for user in users:
        name = user["name"]
        age = user["age"]

        try:
            if age >= 18:
                print(f"{name} es un adulto")
            else:
                print(f"{name} es un menor")

        except KeyError:
            print("La información del usuario está incompleta")

        finally:
            print("Proceso finalizado para el usuario:", name)
