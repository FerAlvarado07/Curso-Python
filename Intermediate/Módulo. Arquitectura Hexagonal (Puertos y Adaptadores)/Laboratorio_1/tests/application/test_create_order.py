from uuid import UUID

import pytest

from src.application.use_cases.create_order import (
    CreateOrder,
    CreateOrderRequest,
)
from src.infrastructure.database.memory_order_repository import (
    MemoryOrderRepository,
)


class FakeNotification:
    def __init__(self) -> None:
        self.notifications: list[tuple[UUID, str]] = []

    def notify_order_created(
        self,
        order_id: UUID,
        customer_name: str,
    ) -> None:
        self.notifications.append((order_id, customer_name))


def test_create_order_saves_and_notifies() -> None:
    repository = MemoryOrderRepository()
    notification = FakeNotification()

    use_case = CreateOrder(
        repository=repository,
        notification=notification,
    )

    result = use_case.execute(
        CreateOrderRequest(
            customer_name="Alex",
            product="Keyboard",
            amount=1200,
        )
    )

    saved_order = repository.find_by_id(result.id)

    assert saved_order is not None
    assert saved_order.customer_name == "Alex"
    assert saved_order.status == "PENDING"

    assert result.id == saved_order.id
    assert result.amount == 1200

    assert notification.notifications == [(result.id, "Alex")]


def test_create_order_rejects_invalid_amount() -> None:
    repository = MemoryOrderRepository()
    notification = FakeNotification()

    use_case = CreateOrder(
        repository=repository,
        notification=notification,
    )

    with pytest.raises(ValueError, match="mayor que cero"):
        use_case.execute(
            CreateOrderRequest(
                customer_name="Alex",
                product="Keyboard",
                amount=0,
            )
        )

    assert repository.orders == {}
    assert notification.notifications == []
