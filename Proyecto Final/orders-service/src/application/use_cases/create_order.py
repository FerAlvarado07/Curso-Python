from src.application.dtos.order_dto import (
    CreateOrderDTO,
    OrderResponseDTO,
)
from src.domain.entities.order import Order
from src.domain.ports.notification import OrderNotification
from src.domain.ports.order_repository import OrderRepository


class CreateOrderUseCase:
    def __init__(
        self,
        repository: OrderRepository,
        notification: OrderNotification,
    ) -> None:
        self._repository = repository
        self._notification = notification

    def execute(self, request: CreateOrderDTO) -> OrderResponseDTO:
        order = Order.create(
            customer_id=request.customer_id,
            amount=request.amount,
            currency=request.currency,
        )

        saved_order = self._repository.save(order)
        self._notification.send_order_created(saved_order)

        return OrderResponseDTO.from_entity(saved_order)
