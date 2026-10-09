from fastapi.testclient import TestClient

from main import app
from src.api.dependencies import (
    get_notification_adapter,
    get_order_repository,
)
from src.infrastructure.database.memory_order_repository import (
    MemoryOrderRepository,
)
from src.infrastructure.http.notification_adapter import (
    HttpNotificationAdapter,
    create_simulated_http_client,
)


def test_create_order_endpoint() -> None:
    repository = MemoryOrderRepository()

    def override_repository():
        yield repository

    def override_notification():
        with create_simulated_http_client() as client:
            yield HttpNotificationAdapter(
                base_url="https://notifications.example.test",
                client=client,
            )

    app.dependency_overrides[get_order_repository] = override_repository
    app.dependency_overrides[get_notification_adapter] = override_notification

    try:
        with TestClient(app) as client:
            response = client.post(
                "/orders",
                json={
                    "customer_name": "Alex",
                    "product": "Keyboard",
                    "amount": 1200,
                },
            )

        assert response.status_code == 201

        data = response.json()

        assert data["customer_name"] == "Alex"
        assert data["product"] == "Keyboard"
        assert data["amount"] == 1200
        assert data["status"] == "PENDING"
        assert len(repository.orders) == 1

    finally:
        app.dependency_overrides.clear()


def test_create_order_rejects_invalid_amount() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/orders",
            json={
                "customer_name": "Alex",
                "product": "Keyboard",
                "amount": -10,
            },
        )

    assert response.status_code == 422
