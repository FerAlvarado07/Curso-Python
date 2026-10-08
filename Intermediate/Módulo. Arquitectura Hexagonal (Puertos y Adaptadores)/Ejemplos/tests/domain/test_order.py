import pytest

from src.domain.entities.order import Order


def test_create_order() -> None:
    order = Order.create(
        customer_name="Fernando",
        product="Laptop",
        amount=15000,
    )

    assert order.customer_name == "Fernando"
    assert order.product == "Laptop"
    assert order.amount == 15000
    assert order.status == "PENDING"


def test_order_can_be_confirmed() -> None:
    order = Order.create(
        customer_name="Fernando",
        product="Laptop",
        amount=15000,
    )

    order.confirm()

    assert order.status == "CONFIRMED"


def test_order_cannot_have_negative_amount() -> None:
    with pytest.raises(ValueError):
        Order.create(
            customer_name="Fernando",
            product="Laptop",
            amount=-100,
        )


def test_order_requires_customer_name() -> None:
    with pytest.raises(ValueError):
        Order.create(
            customer_name="",
            product="Laptop",
            amount=1000,
        )
