from src.application.use_cases.create_order import CreateOrderUseCase
from src.infrastructure.database.postgres_order_repository import (
    PostgresOrderRepository,
)
from src.infrastructure.http.payment_adapter import PaymentHttpAdapter

order_repository = PostgresOrderRepository()
payment_provider = PaymentHttpAdapter()


def get_create_order_use_case() -> CreateOrderUseCase:
    """Construye el caso de uso con sus dependencias."""

    return CreateOrderUseCase(
        order_repository=order_repository,
        payment_provider=payment_provider,
    )
