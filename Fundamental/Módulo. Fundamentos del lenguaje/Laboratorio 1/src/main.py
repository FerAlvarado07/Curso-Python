import json


def read_json_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"No se encontró el archivo: {filename}")
        return None

    except json.JSONDecodeError:
        print(f"El archivo {filename} no contiene un JSON válido")
        return None

    except OSError:
        print(f"No se pudo abrir el archivo: {filename}")
        return None


def filter_users(users):
    return [user for user in users if user["age"] >= 18]


def calculate_total_score(users):
    return sum(user["score"] for user in users)


def calculate_average_score(users):
    if not users:
        return 0

    total_score = calculate_total_score(users)

    return total_score / len(users)


def main():
    filename = "users.json"

    users = read_json_file(filename)

    if users is None:
        return

    print("Usuarios encontrados:")
    print(users)

    adults = filter_users(users)

    print("\nUsuarios mayores de edad:")

    for user in adults:
        print(f"{user['name']} - {user['age']} años")

    total_score = calculate_total_score(users)

    print("\nPuntuación total:")
    print(total_score)

    average_score = calculate_average_score(users)

    print("\nPuntuación promedio:")
    print(average_score)


if __name__ == "__main__":
    main()
