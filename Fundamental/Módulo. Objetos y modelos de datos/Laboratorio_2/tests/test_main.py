from src.main import Order, OrderIn, OrderOut


def test_order_in_to_entity():
    order_in = OrderIn(
        customer="Fernando",
        items=[
            {
                "name": "Laptop",
                "price": 15000,
                "quantity": 1,
            },
        ],
        discount=10,
    )

    order = order_in.to_entity(order_id=1)

    assert isinstance(order, Order)
    assert order.order_id == 1
    assert order.customer == "Fernando"
    assert order.subtotal == 15000
    assert order.discount_amount == 1500
    assert order.total == 13500


def test_order_out_from_entity():
    order = Order(
        order_id=1,
        customer="Fernando",
        items=[
            {
                "name": "Laptop",
                "price": 15000,
                "quantity": 1,
            },
        ],
        discount=10,
    )

    order_out = OrderOut.from_entity(order)

    assert isinstance(order_out, OrderOut)
    assert order_out.order_id == 1
    assert order_out.customer == "Fernando"
    assert order_out.subtotal == 15000
    assert order_out.discount == 1500
    assert order_out.total == 13500
