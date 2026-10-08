import pytest

from src.main import (
    CheckoutService,
    DiscountPricing,
    ExternalPaymentProvider,
    PaymentProviderAdapter,
    PriceService,
    RegularPricing,
    TaxPricing,
    calculate_expensive_price,
)


def test_regular_pricing() -> None:
    strategy = RegularPricing()
    service = PriceService(strategy)

    result = service.get_price(100)

    assert result == 100


def test_discount_pricing() -> None:
    strategy = DiscountPricing(discount=0.20)

    service = PriceService(strategy)

    result = service.get_price(100)

    assert result == 80


def test_tax_pricing() -> None:
    strategy = TaxPricing(tax=0.16)

    service = PriceService(strategy)

    result = service.get_price(100)

    assert result == pytest.approx(116)


def test_cache_returns_same_result() -> None:
    first_result = calculate_expensive_price(100)

    second_result = calculate_expensive_price(100)

    assert first_result == pytest.approx(116)
    assert second_result == pytest.approx(116)


def test_payment_provider_adapter() -> None:
    external_provider = ExternalPaymentProvider()

    adapter = PaymentProviderAdapter(external_provider)

    service = CheckoutService(adapter)

    result = service.checkout(150)

    assert result == "SUCCESS"
