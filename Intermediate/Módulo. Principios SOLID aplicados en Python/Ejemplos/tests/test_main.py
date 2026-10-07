from src.main import (
    FakeRepository,
    OrderService,
)


def test_order_service():
    repository = FakeRepository()
    service = OrderService(repository)

    service.create_order("Order #123")

    assert repository.saved_data == ["Order #123"]
