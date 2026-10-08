from uuid import uuid4

from src.domain.entities.order import Order
from src.infrastructure.database.postgres_order_repository import (
    PostgresOrderRepository,
)


def test_order_repository_contract() -> None:
    repository = PostgresOrderRepository()

    order = Order(
        id=uuid4(),
        customer_name="Fernando",
        product="Laptop",
        amount=15000,
        status="CONFIRMED",
    )

    saved_order = repository.save(order)

    assert saved_order.id == order.id

    found_order = repository.find_by_id(order.id)

    assert found_order is not None
    assert found_order.id == order.id
    assert found_order.customer_name == "Fernando"
