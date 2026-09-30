# Librería estándar y E/S

import csv
import json
import logging
import logging.config
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

# 1. pathlib y manejo de archivos

# pathlib forma parte de la librería estándar de Python
# y permite trabajar con rutas y archivos de forma orientada a objetos.

# Crear una ruta

file_path = Path("data/users.txt")

print(file_path)


# Obtener información de una ruta

print("Nombre:", file_path.name)
print("Extensión:", file_path.suffix)
print("Carpeta:", file_path.parent)


# Comprobar si existe

if file_path.exists():
    print("El archivo existe")
else:
    print("El archivo no existe")


# Comprobar si es un archivo

if file_path.is_file():
    print("Es un archivo")


# Comprobar si es una carpeta

if file_path.is_dir():
    print("Es una carpeta")


# Crear una carpeta

data_path = Path("data")

data_path.mkdir(
    parents=True,
    exist_ok=True,
)


# Escribir un archivo

file_path.write_text(
    "Hola, Python",
    encoding="utf-8",
)


# Leer un archivo

content = file_path.read_text(
    encoding="utf-8",
)

print(content)


# Trabajar con varias líneas

lines = [
    "Python",
    "Angular",
    "React",
]

file_path.write_text(
    "\n".join(lines),
    encoding="utf-8",
)


# Leer líneas

content = file_path.read_text(
    encoding="utf-8",
)

lines = content.splitlines()

print(lines)


# Listar archivos de una carpeta

for file in data_path.iterdir():
    print(file)


# Buscar archivos con una extensión

for file in data_path.glob("*.txt"):
    print(file)


# Buscar archivos recursivamente

for file in data_path.rglob("*.txt"):
    print(file)


# Eliminar un archivo

if file_path.exists():
    file_path.unlink()


# 2. CSV

# Escribir un CSV

users = [
    {
        "name": "Fernando",
        "age": 27,
    },
    {
        "name": "Ana",
        "age": 30,
    },
]

csv_path = Path("data/users.csv")

with csv_path.open(
    "w",
    newline="",
    encoding="utf-8",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["name", "age"],
    )

    writer.writeheader()

    writer.writerows(users)


# Leer un CSV

with csv_path.open(
    "r",
    newline="",
    encoding="utf-8",
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)


# Parseo

# Parsear significa convertir datos en memoria a una estructura
# que nuestro programa pueda utilizar.

# Ejemplo:

# CSV:
#
# name,age
# Fernando,27
# Ana,30
#
# ↓
#
# Python:
#
# {
#     "name": "Fernando",
#     "age": "27"
# }


# Serialización

# Serializar significa convertir una estructura de datos
# de Python a un formato que pueda almacenarse o transmitirse.

# Python:
#
# {
#     "name": "Fernando",
#     "age": 27
# }
#
# ↓
#
# CSV / JSON


# 3. JSON

# JSON significa JavaScript Object Notation.

# Datos Python

user = {
    "name": "Fernando",
    "age": 27,
    "skills": [
        "Python",
        "Angular",
    ],
}


# Serialización a JSON

json_data = json.dumps(
    user,
    ensure_ascii=False,
    indent=4,
)

print(json_data)


# Deserialización de JSON

data = json.loads(json_data)

print(data)
print(data["name"])


# Escribir JSON en un archivo

json_path = Path("data/user.json")

with json_path.open(
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        user,
        file,
        ensure_ascii=False,
        indent=4,
    )


# Leer JSON desde un archivo

with json_path.open(
    "r",
    encoding="utf-8",
) as file:
    data = json.load(file)

print(data)


# Conceptos importantes:
#
# dumps()
# Convierte un objeto Python a un string JSON.
#
# loads()
# Convierte un string JSON a un objeto Python.
#
# dump()
# Escribe un objeto Python directamente en un archivo JSON.
#
# load()
# Lee un archivo JSON y lo convierte en un objeto Python.


# 4. YAML

# YAML es un formato utilizado frecuentemente para configuración.

# Ejemplo:
#
# name: Fernando
# age: 27
# skills:
#   - Python
#   - Angular


# Datos Python

config = {
    "app": {
        "name": "Mi aplicación",
        "debug": True,
    },
    "database": {
        "host": "localhost",
        "port": 5432,
    },
}


# Serialización a YAML

yaml_data = yaml.dump(
    config,
    allow_unicode=True,
    sort_keys=False,
)

print(yaml_data)


# Deserialización de YAML

data = yaml.safe_load(yaml_data)

print(data)


# Escribir YAML

yaml_path = Path("data/config.yaml")

with yaml_path.open(
    "w",
    encoding="utf-8",
) as file:
    yaml.safe_dump(
        config,
        file,
        allow_unicode=True,
        sort_keys=False,
    )


# Leer YAML

with yaml_path.open(
    "r",
    encoding="utf-8",
) as file:
    config = yaml.safe_load(file)

print(config)


# 5. datetime

# datetime permite trabajar con:
#
# - Fechas
# - Horas
# - Fechas y horas
# - Diferencias de tiempo
# - Zonas horarias

mexico_timezone = ZoneInfo("America/Mexico_City")


def get_mexico_time() -> datetime:
    return datetime.now(
        tz=ZoneInfo("America/Mexico_City"),
    )


# Fecha actual

today = datetime.now(
    tz=mexico_timezone,
).date()

print(today)


# Fecha y hora actual

now = datetime.now(
    tz=mexico_timezone,
)

print(now)


# Crear una fecha

birthday = date(
    1999,
    5,
    20,
)

print(birthday)


# Crear una fecha y hora

event_date = datetime(
    2026,
    9,
    30,
    10,
    30,
    tzinfo=mexico_timezone,
)

print(event_date)


# Operaciones con fechas

tomorrow = today + timedelta(days=1)

print(tomorrow)


next_week = today + timedelta(days=7)

print(next_week)


# Diferencia entre fechas

start = date(
    2026,
    9,
    1,
)

end = date(
    2026,
    9,
    30,
)

difference = end - start

print("Días:", difference.days)


# Formatear fechas

formatted = now.strftime(
    "%d/%m/%Y %H:%M:%S",
)

print(formatted)


# Convertir un string a datetime

date_string = "30/09/2026 10:30:00"

parsed_date = datetime.strptime(
    date_string,
    "%d/%m/%Y %H:%M:%S",
).replace(
    tzinfo=mexico_timezone,
)

print(parsed_date)


# 6. Zonas horarias

# Hora en Ciudad de México

mexico_time = datetime.now(
    tz=ZoneInfo("America/Mexico_City"),
)

print(mexico_time)


# Hora en Nueva York

new_york_time = datetime.now(
    tz=ZoneInfo("America/New_York"),
)

print(new_york_time)


# Hora en Londres

london_time = datetime.now(
    tz=ZoneInfo("Europe/London"),
)

print(london_time)


# Convertir una hora entre zonas

current_mexico_time = datetime.now(
    tz=ZoneInfo("America/Mexico_City"),
)

current_new_york_time = current_mexico_time.astimezone(
    ZoneInfo("America/New_York"),
)

print(current_mexico_time)
print(current_new_york_time)


# Un datetime "naive" no contiene información de zona horaria.
#
# Un datetime "aware" contiene información de zona horaria.
#
# Para aplicaciones reales es recomendable trabajar con fechas
# conscientes de zona horaria cuando el contexto lo requiere.


# 7. logging

# logging permite registrar información durante la ejecución
# de una aplicación.
#
# Es preferible utilizar logging en aplicaciones reales
# en lugar de utilizar print() para diagnosticar problemas.


# Configuración básica

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# Diferentes niveles

logger.debug("Mensaje de debug")

logger.info("Aplicación iniciada")

logger.warning("El archivo no existe")

logger.error("No fue posible procesar el archivo")

logger.critical("Error crítico")


# Niveles de logging:
#
# DEBUG
# Información detallada para diagnóstico.
#
# INFO
# Información general de ejecución.
#
# WARNING
# Situación que puede requerir atención.
#
# ERROR
# Se produjo un error.
#
# CRITICAL
# Error grave que puede impedir continuar la aplicación.


# 8. Logging en archivos

# Para guardar logs en un archivo podemos utilizar
# un FileHandler dentro de una configuración personalizada.


# 9. Configuración de logging

# Para aplicaciones más grandes podemos utilizar
# logging.config.

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


# Aplicar configuración

logging.config.dictConfig(
    logging_config,
)


logger.info("Configuración de logging aplicada")


# 10. subprocess

# subprocess permite ejecutar procesos externos
# desde Python.


# Ejecutar un comando

result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    check=False,
)

print(result.stdout)


# Obtener el código de salida

print("Código:", result.returncode)


# Ejecutar un comando y lanzar una excepción
# si ocurre un error

subprocess.run(
    ["python", "--version"],
    check=True,
)


# Capturar stdout y stderr

result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True,
    check=False,
)

print("Salida:", result.stdout)
print("Error:", result.stderr)


# 11. Automatización con subprocess

# Podemos utilizar subprocess para automatizar tareas
# como ejecutar comandos de Git, Poetry, Docker, etc.


# Ejecutar Git

result = subprocess.run(
    ["git", "status"],
    capture_output=True,
    text=True,
    check=True,
)

print(result.stdout)


# Ejecutar pytest desde Python

result = subprocess.run(
    ["python", "-m", "pytest"],
    capture_output=True,
    text=True,
    check=False,
)

print(result.stdout)


# Ejecutar Ruff

result = subprocess.run(
    ["python", "-m", "ruff", "check", "."],
    capture_output=True,
    text=True,
    check=False,
)

print(result.stdout)


# 12. Diferencia entre parseo y serialización

# Parseo:
#
# Formato externo
#       ↓
# Python
#
# Ejemplo:
#
# JSON
#   ↓
# dict
#
# json.loads()


# Serialización:
#
# Python
#   ↓
# Formato externo
#
# Ejemplo:
#
# dict
#   ↓
# JSON
#
# json.dumps()


data = {
    "name": "Fernando",
    "age": 27,
}


# Serialización

json_data = json.dumps(data)

print(json_data)


# Parseo

python_data = json.loads(json_data)

print(python_data)
