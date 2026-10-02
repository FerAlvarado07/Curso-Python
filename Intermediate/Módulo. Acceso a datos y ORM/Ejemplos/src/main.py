from src import (
    sqlalchemy_core_example,
    sqlalchemy_orm_example,
    sqlalchemy_relations,
    sqlite_example,
)


def main() -> None:
    print("Módulo. Acceso a datos y ORM")
    print()
    print("1. SQLite")
    print("2. SQLAlchemy Core")
    print("3. SQLAlchemy ORM")
    print("4. SQLAlchemy Relaciones")

    option = input("\nSelecciona una opción: ")

    if option == "1":
        sqlite_example.main()

    elif option == "2":
        sqlalchemy_core_example.main()

    elif option == "3":
        sqlalchemy_orm_example.main()

    elif option == "4":
        sqlalchemy_relations.main()

    else:
        print("Opción no válida")


if __name__ == "__main__":
    main()
