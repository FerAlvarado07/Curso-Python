from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Order:
    id: UUID
    customer_name: str
    product: str
    amount: float
    status: str = "PENDING"

    @classmethod
    def create(
        cls,
        customer_name: str,
        product: str,
        amount: float,
    ) -> "Order":
        if not customer_name.strip():
            raise ValueError("Comprador es requerido")

        if not product.strip():
            raise ValueError("Producto es requerido")

        if amount <= 0:
            raise ValueError("Monto debe ser mayor que cero")

        return cls(
            id=uuid4(),
            customer_name=customer_name,
            product=product,
            amount=amount,
        )
