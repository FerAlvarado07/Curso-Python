class PaymentHttpAdapter:
    """Adapter para comunicarse con un servicio externo de pagos."""

    def process_payment(self, amount: float) -> bool:
        """Simula una llamada HTTP al proveedor de pagos."""

        print(f"Processing payment of ${amount}")

        # Aquí normalmente se utiliza httpx.
        return True
