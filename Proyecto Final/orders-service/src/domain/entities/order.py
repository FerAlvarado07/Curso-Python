from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from src.domain.exceptions.order_exceptions import InvalidOrderError


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Order:
    id: UUID
    customer_id: str
    amount: Decimal
    currency: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        customer_id: str,
        amount: Decimal,
        currency: str = "MXN",
    ) -> "Order":
        if not customer_id.strip():
            raise InvalidOrderError("El identificador del cliente es obligatorio.")

        if amount <= Decimal("0"):
            raise InvalidOrderError("El monto debe ser mayor que cero.")

        normalized_currency = currency.strip().upper()

        if len(normalized_currency) != 3 or not normalized_currency.isalpha():
            raise InvalidOrderError("La moneda debe ser un código de tres letras.")

        now = datetime.now(UTC)

        return cls(
            id=uuid4(),
            customer_id=customer_id.strip(),
            amount=amount.quantize(Decimal("0.01")),
            currency=normalized_currency,
            status=OrderStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise InvalidOrderError("Solo se pueden confirmar órdenes pendientes.")

        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.now(UTC)

    def cancel(self) -> None:
        if self.status == OrderStatus.CANCELLED:
            raise InvalidOrderError("La orden ya está cancelada.")

        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now(UTC)
