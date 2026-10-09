from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


def test_register_login_and_access_protected_endpoint():
    email = f"user-{uuid4().hex}@example.com"
    password = "StrongPassword123"

    with TestClient(app) as client:
        register_response = client.post(
            "/auth/register",
            json={"email": email, "password": password},
        )
        assert register_response.status_code == 201

        login_response = client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]
        assert token

        orders_response = client.get(
            "/orders",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert orders_response.status_code == 200


def test_protected_endpoint_rejects_missing_token():
    with TestClient(app) as client:
        response = client.get("/orders")

    assert response.status_code == 401
