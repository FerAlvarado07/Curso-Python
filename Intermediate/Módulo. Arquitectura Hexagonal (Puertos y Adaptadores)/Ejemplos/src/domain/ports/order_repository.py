from typing import Protocol
from uuid import UUID

from src.domain.entities.order import Order


class OrderRepository(Protocol):
    """Puerto para persistir órdenes."""

    def save(self, order: Order) -> Order:
        """Guarda una orden."""
        ...

    def find_by_id(self, order_id: UUID) -> Order | None:
        """Busca una orden por su identificador."""
        ...
