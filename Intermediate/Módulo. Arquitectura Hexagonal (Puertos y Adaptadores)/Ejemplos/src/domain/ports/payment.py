from typing import Protocol


class PaymentProvider(Protocol):
    """Puerto para procesar pagos."""

    def process_payment(self, amount: float) -> bool:
        """Procesa un pago."""
        ...
