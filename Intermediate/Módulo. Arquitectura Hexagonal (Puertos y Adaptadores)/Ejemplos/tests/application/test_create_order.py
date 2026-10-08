from src.application.dtos.order_dto import CreateOrderRequest
from src.application.use_cases.create_order import CreateOrderUseCase
from src.domain.entities.order import Order


class FakeOrderRepository:
    """Fake utilizado para probar el caso de uso."""

    def __init__(self) -> None:
        self.orders: list[Order] = []

    def save(self, order: Order) -> Order:
        self.orders.append(order)
        return order


class FakePaymentProvider:
    """Fake utilizado para simular pagos."""

    def process_payment(self, amount: float) -> bool:
        return True


def test_create_order_use_case() -> None:
    repository = FakeOrderRepository()
    payment_provider = FakePaymentProvider()

    use_case = CreateOrderUseCase(
        order_repository=repository,
        payment_provider=payment_provider,
    )

    request = CreateOrderRequest(
        customer_name="Fernando",
        product="Laptop",
        amount=15000,
    )

    result = use_case.execute(request)

    assert result.customer_name == "Fernando"
    assert result.product == "Laptop"
    assert result.amount == 15000
    assert result.status == "CONFIRMED"

    assert len(repository.orders) == 1
