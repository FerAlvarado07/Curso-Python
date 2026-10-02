from datetime import datetime


def show_migration_concept() -> None:
    print("Alembic")
    print()
    print("Las migraciones permiten modificar")
    print("el esquema de la base de datos")
    print("sin eliminar la información existente.")
    print()

    print("Ejemplo:")
    print()
    print("Versión 1:")
    print("users")
    print("  - id")
    print("  - name")
    print("  - email")
    print()

    print("Versión 2:")
    print("users")
    print("  - id")
    print("  - name")
    print("  - email")
    print("  - created_at")
    print()

    print(f"Fecha del ejemplo: {datetime.now()}")


def main() -> None:
    show_migration_concept()


if __name__ == "__main__":
    main()
