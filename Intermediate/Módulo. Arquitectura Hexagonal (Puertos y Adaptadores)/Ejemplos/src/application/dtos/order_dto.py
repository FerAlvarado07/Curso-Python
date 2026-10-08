from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateOrderRequest:
    """DTO utilizado para crear una orden."""

    customer_name: str
    product: str
    amount: float


@dataclass
class OrderResponse:
    """DTO utilizado como respuesta."""

    id: UUID
    customer_name: str
    product: str
    amount: float
    status: str
