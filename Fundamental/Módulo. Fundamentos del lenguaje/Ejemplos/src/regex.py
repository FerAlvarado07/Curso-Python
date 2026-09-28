import re

# 1. search() -> busca una coincidencia

text = "My phone number is 5512345678"

result = re.search(r"\d+", text)

if result:
    print("search():", result.group())


# 2. match() -> busca una coincidencia al inicio

text = "Hello Python"

result = re.match(r"Hello", text)

if result:
    print("match():", result.group())


# 3. findall() -> obtiene todas las coincidencias

text = "My numbers are 123, 456 and 789"

result = re.findall(r"\d+", text)

print("findall():", result)


# 4. sub() -> reemplaza coincidencias

text = "My phone is 5512345678"

result = re.sub(r"\d", "*", text)

print("sub():", result)


# 5. . -> cualquier carácter

text = "cat cot cut"

result = re.findall(r"c.t", text)

print("Resultado:", result)


# 6. \d -> dígitos

text = "My age is 28"

result = re.findall(r"\d", text)

print("Dígitos encontrados:", result)


# 7. \D -> cualquier cosa que NO sea un dígito

text = "ABC123"

result = re.findall(r"\D+", text)

print("Caracteres que no son dígitos:", result)


# 8. \w -> caracteres alfanuméricos y _

text = "hello world_123"

result = re.findall(r"\w+", text)

print("Caracteres alfanuméricos encontrados:", result)


# 9. \s -> espacios, tabs y saltos de línea

text = "Hello World Python"

result = re.findall(r"\s", text)

print("Espacios encontrados:", result)


# 10. + -> uno o más

text = "123 abc 4567"

result = re.findall(r"\d+", text)

print("Uno o más dígitos:", result)


# 11. * -> cero o más

text = "ab a abb"

result = re.findall(r"ab*", text)

print("Cero o más coincidencias:", result)


# 12. ? -> cero o uno

text = "color colour"

result = re.findall(r"colou?r", text)

print("Coincidencias opcionales:", result)


# 13. {n} -> exactamente n veces

text = "123 1234 12345"

result = re.findall(r"\d{4}", text)

print("Coincidencias de exactamente 4 dígitos:", result)


# 14. {n,m} -> entre n y m veces

text = "12 123 1234 12345 123456"

result = re.findall(r"\d{3,5}", text)

print("Coincidencias de 3 a 5 dígitos:", result)


# 15. [] -> conjunto de caracteres

text = "cat bat hat rat"

result = re.findall(r"[cb]at", text)

print("Coincidencias del conjunto:", result)


# 16. [a-z] -> letras minúsculas

text = "hello Python WORLD"

result = re.findall(r"[a-z]+", text)

print("Letras minúsculas:", result)


# 17. [A-Z] -> letras mayúsculas

text = "hello Python WORLD"

result = re.findall(r"[A-Z]+", text)

print("Letras mayúsculas:", result)


# 18. [0-9] -> números

text = "Product123"

result = re.findall(r"[0-9]+", text)

print("Números encontrados:", result)


# 19. [^...] -> cualquier carácter que NO pertenezca al conjunto

text = "ABC123"

result = re.findall(r"[^0-9]+", text)

print("Caracteres que no son números:", result)


# 20. ^ -> inicio del texto

text = "Python is awesome"

result = re.search(r"^Python", text)

if result:
    print("El texto comienza con Python")


# 21. $ -> final del texto

text = "I love Python"

result = re.search(r"Python$", text)

if result:
    print("El texto termina con Python")


# 22. () -> grupos

text = "Name: Fernando, Age: 28"

result = re.search(r"Name: (\w+), Age: (\d+)", text)

if result:
    name = result.group(1)
    age = result.group(2)

    print("Nombre:", name)
    print("Edad:", age)


# 23. Validar un email

email = "fernando@example.com"

pattern = r"^[\w.-]+@[\w.-]+\.\w+$"

if re.match(pattern, email):
    print("El correo electrónico es válido")
else:
    print("El correo electrónico no es válido")


# 24. Validar un teléfono mexicano de 10 dígitos

phone = "5512345678"

pattern = r"^\d{10}$"

if re.match(pattern, phone):
    print("El teléfono es válido")
else:
    print("El teléfono no es válido")


# 25. Extraer una edad de un texto

text = "Fernando is 28 years old"

result = re.search(r"(\d+) years old", text)

if result:
    age = result.group(1)

    print("Edad encontrada:", age)


# 26. Extraer teléfonos de un texto

text = """
Contact:
Fernando: 5512345678
Carlos: 5587654321
Ana: 5511122233
"""

phones = re.findall(r"\b\d{10}\b", text)

print("Teléfonos encontrados:", phones)


# 27. Extraer emails de un texto

text = """
Contact us at support@example.com
or admin@company.com
"""

emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", text)

print("Correos encontrados:", emails)


# 28. Extraer números de un texto

text = "Products cost 100, 250 and 999 pesos"

numbers = re.findall(r"\d+", text)

print("Números encontrados:", numbers)


# 29. Extraer palabras

text = "Python is a powerful programming language"

words = re.findall(r"\b\w+\b", text)

print("Palabras encontradas:", words)


# 30. Ejemplo completo

text = """
Name: Fernando
Age: 28
Email: fernando@example.com
Phone: 5512345678
"""

name = re.search(r"Name:\s*(\w+)", text)
age = re.search(r"Age:\s*(\d+)", text)
email = re.search(r"Email:\s*([\w.-]+@[\w.-]+\.\w+)", text)
phone = re.search(r"Phone:\s*(\d{10})", text)

if name:
    print("Nombre:", name.group(1))

if age:
    print("Edad:", age.group(1))

if email:
    print("Correo:", email.group(1))

if phone:
    print("Teléfono:", phone.group(1))


# 31. r"..." -> raw string

pattern = r"\d+"

text = "There are 123 users"

result = re.findall(pattern, text)

print("Resultado usando raw string:", result)
