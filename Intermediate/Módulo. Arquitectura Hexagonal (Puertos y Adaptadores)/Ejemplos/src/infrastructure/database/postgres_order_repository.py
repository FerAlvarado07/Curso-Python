from uuid import UUID

from src.domain.entities.order import Order


class PostgresOrderRepository:
    """Adapter encargado de persistir órdenes."""

    def __init__(self) -> None:
        # Simula una tabla de PostgreSQL.
        self.orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> Order:
        """Guarda la orden."""

        self.orders[order.id] = order

        return order

    def find_by_id(self, order_id: UUID) -> Order | None:
        """Busca una orden."""

        return self.orders.get(order_id)
