from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.models.order import Order, OrderItem
from src.schemas.order import OrderCreate, OrderUpdate


def create_order(
    session: Session,
    user_id: int,
    order_data: OrderCreate,
) -> Order:
    order = Order(
        user_id=user_id,
        status="pending",
    )

    for item_data in order_data.items:
        item = OrderItem(
            product=item_data.product,
            quantity=item_data.quantity,
            price=item_data.price,
        )

        order.items.append(item)

    session.add(order)
    session.commit()

    session.refresh(order)

    return order


def get_orders(
    session: Session,
    user_id: int,
) -> list[Order]:
    statement = (
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.items))
        .order_by(Order.id)
    )

    return list(session.scalars(statement))


def get_order(
    session: Session,
    order_id: int,
    user_id: int,
) -> Order | None:
    statement = (
        select(Order)
        .where(
            Order.id == order_id,
            Order.user_id == user_id,
        )
        .options(selectinload(Order.items))
    )

    return session.scalars(statement).first()


def update_order(
    session: Session,
    order: Order,
    order_data: OrderUpdate,
) -> Order:
    order.status = order_data.status

    session.commit()
    session.refresh(order)

    return order


def delete_order(
    session: Session,
    order: Order,
) -> None:
    session.delete(order)
    session.commit()


def get_order_total(order: Order) -> Decimal:
    return sum(
        (item.subtotal for item in order.items),
        Decimal("0.00"),
    )
