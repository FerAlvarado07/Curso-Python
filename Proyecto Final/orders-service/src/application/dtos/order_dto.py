from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.domain.entities.order import Order, OrderStatus


@dataclass(frozen=True)
class CreateOrderDTO:
    customer_id: str
    amount: Decimal
    currency: str = "MXN"


@dataclass(frozen=True)
class OrderResponseDTO:
    id: UUID
    customer_id: str
    amount: Decimal
    currency: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, order: Order) -> "OrderResponseDTO":
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            amount=order.amount,
            currency=order.currency,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


@dataclass(frozen=True)
class OrderListDTO:
    items: list[OrderResponseDTO]
    total: int
    offset: int
    limit: int
