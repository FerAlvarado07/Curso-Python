from dataclasses import dataclass


@dataclass
class Order:
    order_id: int
    customer: str
    items: list[dict]
    discount: float = 0

    @property
    def subtotal(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    @property
    def discount_amount(self):
        return self.subtotal * (self.discount / 100)

    @property
    def total(self):
        return self.subtotal - self.discount_amount

    def __eq__(self, other):
        if not isinstance(other, Order):
            return NotImplemented

        return self.order_id == other.order_id

    def __lt__(self, other):
        if not isinstance(other, Order):
            return NotImplemented

        return self.total < other.total


if __name__ == "__main__":
    order1 = Order(
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

    order2 = Order(
        order_id=2,
        customer="Ana",
        items=[
            {
                "name": "Monitor",
                "price": 5000,
                "quantity": 2,
            },
        ],
        discount=5,
    )

    print("Pedido 1")
    print("Cliente:", order1.customer)
    print("Subtotal:", order1.subtotal)
    print("Descuento:", order1.discount_amount)
    print("Total:", order1.total)

    print("\nPedido 2")
    print("Cliente:", order2.customer)
    print("Subtotal:", order2.subtotal)
    print("Descuento:", order2.discount_amount)
    print("Total:", order2.total)

    print("\nComparaciones")

    print("¿Son el mismo pedido?", order1 == order2)
    print("¿Pedido 1 es menor que pedido 2?", order1 < order2)
