from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateOrderRequest:
    customer_name: str
    product: str
    amount: float


@dataclass
class OrderResponse:
    id: UUID
    customer_name: str
    product: str
    amount: float
    status: str
