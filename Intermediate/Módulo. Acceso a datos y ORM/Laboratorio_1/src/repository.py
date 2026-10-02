from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.models import Order, OrderItem, User


def create_user(
    session: Session,
    name: str,
    email: str,
) -> User:
    user = User(
        name=name,
        email=email,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user(
    session: Session,
    user_id: int,
) -> User | None:
    return session.get(User, user_id)


def get_users(session: Session) -> list[User]:
    statement = select(User).order_by(User.id)

    return list(session.scalars(statement))


def update_user(
    session: Session,
    user_id: int,
    name: str,
    email: str,
) -> User | None:
    user = session.get(User, user_id)

    if user is None:
        return None

    user.name = name
    user.email = email

    session.commit()
    session.refresh(user)

    return user


def delete_user(
    session: Session,
    user_id: int,
) -> bool:
    user = session.get(User, user_id)

    if user is None:
        return False

    session.delete(user)
    session.commit()

    return True


def create_order(
    session: Session,
    user_id: int,
    items: list[dict],
) -> Order:
    order = Order(user_id=user_id)

    for item in items:
        order.items.append(
            OrderItem(
                product=item["product"],
                quantity=item["quantity"],
                price=Decimal(str(item["price"])),
            )
        )

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


def get_order(
    session: Session,
    order_id: int,
) -> Order | None:
    statement = (
        select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    )

    return session.scalar(statement)


def get_orders(session: Session) -> list[Order]:
    statement = select(Order).options(selectinload(Order.items)).order_by(Order.id)

    return list(session.scalars(statement))


def delete_order(
    session: Session,
    order_id: int,
) -> bool:
    order = session.get(Order, order_id)

    if order is None:
        return False

    session.delete(order)
    session.commit()

    return True


def get_order_total(order: Order) -> Decimal:
    return sum(
        (item.subtotal for item in order.items),
        Decimal("0"),
    )
