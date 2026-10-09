from dataclasses import dataclass
from uuid import UUID

from src.domain.entities.order import Order
from src.domain.ports.notification import OrderNotification
from src.domain.ports.order_repository import OrderRepository


@dataclass(frozen=True)
class CreateOrderRequest:
    customer_name: str
    product: str
    amount: float


@dataclass(frozen=True)
class CreateOrderResponse:
    id: UUID
    customer_name: str
    product: str
    amount: float
    status: str


class CreateOrder:
    def __init__(
        self,
        repository: OrderRepository,
        notification: OrderNotification,
    ) -> None:
        self.repository = repository
        self.notification = notification

    def execute(
        self,
        request: CreateOrderRequest,
    ) -> CreateOrderResponse:
        order = Order.create(
            customer_name=request.customer_name,
            product=request.product,
            amount=request.amount,
        )

        saved_order = self.repository.save(order)

        self.notification.notify_order_created(
            order_id=saved_order.id,
            customer_name=saved_order.customer_name,
        )

        return CreateOrderResponse(
            id=saved_order.id,
            customer_name=saved_order.customer_name,
            product=saved_order.product,
            amount=saved_order.amount,
            status=saved_order.status,
        )
