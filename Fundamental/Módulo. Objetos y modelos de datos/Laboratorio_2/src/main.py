from dataclasses import dataclass
from pydantic import BaseModel, Field


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


class OrderItemIn(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderIn(BaseModel):
    customer: str
    items: list[OrderItemIn]
    discount: float = Field(default=0, ge=0, le=100)

    def to_entity(self, order_id: int):
        return Order(
            order_id=order_id,
            customer=self.customer,
            items=[item.model_dump() for item in self.items],
            discount=self.discount,
        )


class OrderOut(BaseModel):
    order_id: int
    customer: str
    subtotal: float
    discount: float
    total: float

    @classmethod
    def from_entity(cls, order: Order):
        return cls(
            order_id=order.order_id,
            customer=order.customer,
            subtotal=order.subtotal,
            discount=order.discount_amount,
            total=order.total,
        )


if __name__ == "__main__":
    data = {
        "customer": "Fernando",
        "items": [
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
        "discount": 10,
    }

    order_in = OrderIn.model_validate(data)

    print("OrderIn:")
    print(order_in)

    order = order_in.to_entity(order_id=1)

    print("\nEntidad Order:")
    print(order)

    print("\nCálculos:")
    print("Subtotal:", order.subtotal)
    print("Descuento:", order.discount_amount)
    print("Total:", order.total)

    order_out = OrderOut.from_entity(order)

    print("\nOrderOut:")
    print(order_out)

    print("\nJSON:")
    print(order_out.model_dump_json())
