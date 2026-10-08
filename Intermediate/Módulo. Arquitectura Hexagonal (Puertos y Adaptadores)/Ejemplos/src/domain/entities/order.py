from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Order:
    """Entidad principal del dominio."""

    id: UUID
    customer_name: str
    product: str
    amount: float
    status: str

    @classmethod
    def create(
        cls,
        customer_name: str,
        product: str,
        amount: float,
    ) -> "Order":
        """Crea una nueva orden aplicando las reglas iniciales."""

        if not customer_name:
            raise ValueError("Customer name is required")

        if not product:
            raise ValueError("Product is required")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        return cls(
            id=uuid4(),
            customer_name=customer_name,
            product=product,
            amount=amount,
            status="PENDING",
        )

    def confirm(self) -> None:
        """Confirma la orden."""

        if self.status != "PENDING":
            raise ValueError("Only pending orders can be confirmed")

        self.status = "CONFIRMED"
