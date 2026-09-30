from src.main import Order


def test_order_calculations():
    order = Order(
        order_id=1,
        customer="Fernando",
        items=[
            {
                "name": "Laptop",
                "price": 15000,
                "quantity": 1,
            },
            {
                "name": "Mouse",
                "price": 500,
                "quantity": 2,
            },
        ],
        discount=10,
    )

    assert order.subtotal == 16000
    assert order.discount_amount == 1600
    assert order.total == 14400


def test_order_comparison():
    order1 = Order(
        order_id=1,
        customer="Fernando",
        items=[
            {
                "name": "Laptop",
                "price": 15000,
                "quantity": 1,
            },
        ],
    )

    order2 = Order(
        order_id=2,
        customer="Ana",
        items=[
            {
                "name": "Monitor",
                "price": 5000,
                "quantity": 1,
            },
        ],
    )

    assert order1 != order2
    assert order2 < order1
