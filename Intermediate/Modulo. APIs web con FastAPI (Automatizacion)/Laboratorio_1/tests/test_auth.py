def test_login_success(client, db_session):
    from src.models.user import User
    from src.services.auth_service import hash_password

    user = User(
        name="Fernando",
        email="fernando@axity.com",
        password_hash=hash_password("12345678"),
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "fernando@axity.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Inicio de sesión exitoso"
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_login_with_invalid_email(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "noexiste@example.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["errorCode"] == "AUTH_001"
    assert data["userError"] == ("No está autorizado para realizar esta operación")


def test_login_with_invalid_password(client, db_session):
    from src.models.user import User
    from src.services.auth_service import hash_password

    user = User(
        name="Fernando",
        email="fernando@axity.com",
        password_hash=hash_password("12345678"),
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "fernando@axity.com",
            "password": "password-incorrecto",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["errorCode"] == "AUTH_001"
