from src.database import create_database, get_session
from src.repository import (
    create_order,
    create_user,
    delete_order,
    delete_user,
    get_order,
    get_order_total,
    get_orders,
    get_user,
    get_users,
    update_user,
)


def main() -> None:
    print("SQLAlchemy ORM - Users / Orders")

    create_database()

    with get_session() as session:
        user = create_user(
            session,
            "Fernando",
            "fernando.alvarado@axity.com",
        )

        print("\nUsuario creado:")
        print(user)

        order = create_order(
            session,
            user.id,
            [
                {
                    "product": "Teclado",
                    "quantity": 1,
                    "price": 850,
                },
                {
                    "product": "Mouse",
                    "quantity": 2,
                    "price": 450,
                },
            ],
        )

        print("\nOrden creada:")
        print(order)

        order = get_order(session, order.id)

        if order:
            print("\nProductos:")

            for item in order.items:
                print(f"- {item.product}: {item.quantity} x ${item.price}")

            print(f"\nTotal: ${get_order_total(order)}")

        print("\nUsuarios:")

        for current_user in get_users(session):
            print(current_user)

        update_user(
            session,
            user.id,
            "Fernando Enrique",
            "fernando.enrique@axity.com",
        )

        print("\nUsuario actualizado:")
        print(get_user(session, user.id))

        print("\nÓrdenes:")

        for current_order in get_orders(session):
            print(
                f"Orden #{current_order.id} - Total: ${get_order_total(current_order)}"
            )

        delete_order(session, order.id)
        delete_user(session, user.id)

        print("\nDatos eliminados.")


if __name__ == "__main__":
    main()
