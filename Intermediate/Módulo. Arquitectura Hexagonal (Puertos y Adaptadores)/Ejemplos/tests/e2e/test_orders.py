from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_order_e2e() -> None:
    response = client.post(
        "/orders",
        json={
            "customer_name": "Fernando",
            "product": "Laptop",
            "amount": 15000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["customer_name"] == "Fernando"
    assert data["product"] == "Laptop"
    assert data["amount"] == 15000
    assert data["status"] == "CONFIRMED"
    assert "id" in data
