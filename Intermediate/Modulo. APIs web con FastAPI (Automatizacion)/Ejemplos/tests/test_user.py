import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services import user_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    """
    Limpia los usuarios antes de cada test.

    Esto evita que los tests dependan del orden
    en que pytest los ejecuta.
    """
    user_service.users.clear()
    user_service._next_id = 1


def create_test_user(
    name: str = "Fernando",
    email: str = "fernando@example.com",
    password: str = "12345678",
) -> dict:
    """
    Crea un usuario de prueba.
    """
    response = client.post(
        "/users/",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    return response.json()


def login_test_user(
    email: str = "fernando@example.com",
    password: str = "12345678",
) -> str:
    """
    Inicia sesión y devuelve el JWT.
    """
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def get_auth_headers(token: str) -> dict:
    """
    Construye el header Authorization.
    """
    return {
        "Authorization": f"Bearer {token}",
    }


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "name": "Fernando",
            "email": "fernando@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Fernando"
    assert data["email"] == "fernando@example.com"

    # La contraseña nunca debe regresar en la respuesta.
    assert "password" not in data
    assert "password_hash" not in data


def test_get_users():
    create_test_user()

    token = login_test_user()

    response = client.get(
        "/users/",
        headers=get_auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Fernando"
    assert data[0]["email"] == "fernando@example.com"


def test_get_user_not_found():
    create_test_user()

    token = login_test_user()

    response = client.get(
        "/users/99999",
        headers=get_auth_headers(token),
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Usuario no encontrado",
    }


def test_get_current_user():
    create_test_user()

    token = login_test_user()

    response = client.get(
        "/users/me",
        headers=get_auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Fernando"
    assert data["email"] == "fernando@example.com"


def test_get_current_user_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401


def test_update_user():
    create_test_user()

    token = login_test_user()

    response = client.put(
        "/users/1",
        json={
            "name": "Fernando Enrique",
            "email": "fernando.enrique@example.com",
        },
        headers=get_auth_headers(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Fernando Enrique"
    assert data["email"] == "fernando.enrique@example.com"


def test_delete_user_without_token():
    create_test_user()

    response = client.delete("/users/1")

    assert response.status_code == 401


def test_delete_user_with_token():
    create_test_user()

    token = login_test_user()

    response = client.delete(
        "/users/1",
        headers=get_auth_headers(token),
    )

    assert response.status_code == 204


def test_login_with_wrong_password():
    create_test_user()

    response = client.post(
        "/auth/login",
        data={
            "username": "fernando@example.com",
            "password": "password-incorrecto",
        },
    )

    assert response.status_code == 401


def test_login_with_unknown_user():
    response = client.post(
        "/auth/login",
        data={
            "username": "noexiste@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 401


def test_invalid_token():
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer token-invalido",
        },
    )

    assert response.status_code == 401
