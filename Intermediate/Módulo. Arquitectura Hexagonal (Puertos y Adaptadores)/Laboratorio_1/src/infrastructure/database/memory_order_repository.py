from uuid import UUID

from src.domain.entities.order import Order


class MemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> Order:
        self.orders[order.id] = order
        return order

    def find_by_id(self, order_id: UUID) -> Order | None:
        return self.orders.get(order_id)
