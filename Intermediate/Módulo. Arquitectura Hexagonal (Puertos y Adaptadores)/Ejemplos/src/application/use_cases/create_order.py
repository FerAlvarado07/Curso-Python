from src.application.dtos.order_dto import (
    CreateOrderRequest,
    OrderResponse,
)
from src.domain.entities.order import Order
from src.domain.ports.order_repository import OrderRepository
from src.domain.ports.payment import PaymentProvider


class CreateOrderUseCase:
    """Caso de uso para crear una orden."""

    def __init__(
        self,
        order_repository: OrderRepository,
        payment_provider: PaymentProvider,
    ) -> None:
        self.order_repository = order_repository
        self.payment_provider = payment_provider

    def execute(self, request: CreateOrderRequest) -> OrderResponse:
        """Ejecuta el proceso completo de creación de una orden."""

        order = Order.create(
            customer_name=request.customer_name,
            product=request.product,
            amount=request.amount,
        )

        payment_successful = self.payment_provider.process_payment(order.amount)

        if not payment_successful:
            raise ValueError("Payment failed")

        order.confirm()

        saved_order = self.order_repository.save(order)

        return OrderResponse(
            id=saved_order.id,
            customer_name=saved_order.customer_name,
            product=saved_order.product,
            amount=saved_order.amount,
            status=saved_order.status,
        )
