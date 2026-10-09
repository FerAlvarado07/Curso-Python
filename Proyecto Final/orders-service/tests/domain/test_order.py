from decimal import Decimal

import pytest

from src.domain.entities.order import Order, OrderStatus
from src.domain.exceptions.order_exceptions import InvalidOrderError


def test_create_order_with_valid_data() -> None:
    order = Order.create("customer-1", Decimal("150.00"))

    assert order.customer_id == "customer-1"
    assert order.amount == Decimal("150.00")
    assert order.currency == "MXN"
    assert order.status == OrderStatus.PENDING


def test_create_order_rejects_invalid_amount() -> None:
    with pytest.raises(InvalidOrderError, match="mayor que cero"):
        Order.create("customer-1", Decimal("0"))


def test_create_order_rejects_empty_customer() -> None:
    with pytest.raises(InvalidOrderError):
        Order.create("  ", Decimal("10"))


def test_confirm_order() -> None:
    order = Order.create("customer-1", Decimal("10"))

    order.confirm()

    assert order.status == OrderStatus.CONFIRMED


def test_cannot_confirm_cancelled_order() -> None:
    order = Order.create("customer-1", Decimal("10"))
    order.cancel()

    with pytest.raises(InvalidOrderError):
        order.confirm()


def test_cancel_order() -> None:
    order = Order.create("customer-1", Decimal("10"))

    order.cancel()

    assert order.status == OrderStatus.CANCELLED
