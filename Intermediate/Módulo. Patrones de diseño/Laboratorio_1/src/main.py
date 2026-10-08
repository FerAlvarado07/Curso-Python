from typing import Protocol


class PricingStrategy(Protocol):
    def calculate_price(
        self,
        base_price: float,
    ) -> float: ...


class RegularPricing:
    def calculate_price(
        self,
        base_price: float,
    ) -> float:
        return base_price


class DiscountPricing:
    def __init__(
        self,
        discount: float,
    ) -> None:
        self.discount = discount

    def calculate_price(
        self,
        base_price: float,
    ) -> float:
        return base_price * (1 - self.discount)


class TaxPricing:
    def __init__(
        self,
        tax: float,
    ) -> None:
        self.tax = tax

    def calculate_price(
        self,
        base_price: float,
    ) -> float:
        return base_price * (1 + self.tax)


class PriceService:
    def __init__(
        self,
        strategy: PricingStrategy,
    ) -> None:
        self.strategy = strategy

    def get_price(
        self,
        base_price: float,
    ) -> float:
        return self.strategy.calculate_price(base_price)


def cache_result(function):
    cache = {}

    def wrapper(*args):
        if args in cache:
            print("Resultado obtenido desde caché")

            return cache[args]

        print("Calculando precio...")

        result = function(*args)

        cache[args] = result

        return result

    return wrapper


@cache_result
def calculate_expensive_price(
    base_price: float,
) -> float:
    print("Ejecutando cálculo costoso...")

    return base_price * 1.16


class ExternalPaymentProvider:
    def make_transaction(
        self,
        amount: float,
    ) -> str:
        print(f"External provider: transaction ${amount}")

        return "SUCCESS"


class PaymentProvider(Protocol):
    def pay(
        self,
        amount: float,
    ) -> str: ...


class PaymentProviderAdapter:
    def __init__(
        self,
        provider: ExternalPaymentProvider,
    ) -> None:
        self.provider = provider

    def pay(
        self,
        amount: float,
    ) -> str:
        return self.provider.make_transaction(amount)


class CheckoutService:
    def __init__(
        self,
        payment_provider: PaymentProvider,
    ) -> None:
        self.payment_provider = payment_provider

    def checkout(
        self,
        amount: float,
    ) -> str:
        return self.payment_provider.pay(amount)


def main() -> None:
    print("\n Strategy:")

    regular_strategy = RegularPricing()

    regular_service = PriceService(regular_strategy)

    print(f"Regular: ${regular_service.get_price(100):.2f}")

    discount_strategy = DiscountPricing(discount=0.20)

    discount_service = PriceService(discount_strategy)

    print(f"20% descuento: ${discount_service.get_price(100):.2f}")

    tax_strategy = TaxPricing(tax=0.16)

    tax_service = PriceService(tax_strategy)

    print(f"16% impuesto: ${tax_service.get_price(100):.2f}")

    print("\n Decorator de caché:")

    print(calculate_expensive_price(100))

    print(calculate_expensive_price(100))

    print("\nAdapter:")

    external_provider = ExternalPaymentProvider()

    adapter = PaymentProviderAdapter(external_provider)

    checkout_service = CheckoutService(adapter)

    result = checkout_service.checkout(150)

    print(f"Resultado: {result}")


if __name__ == "__main__":
    main()
