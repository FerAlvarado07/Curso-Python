def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "Fernando",
            "email": "fernando@axity.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Usuario creado correctamente"

    assert data["data"]["id"] == 1
    assert data["data"]["name"] == "Fernando"
    assert data["data"]["email"] == "fernando@axity.com"

    # Verificamos que nunca se devuelva el password.
    assert "password" not in data["data"]
    assert "password_hash" not in data["data"]


def test_create_user_duplicate_email(client):
    user_data = {
        "name": "Fernando",
        "email": "fernando@axity.com",
        "password": "12345678",
    }

    first_response = client.post(
        "/users/",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users/",
        json=user_data,
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["errorCode"] == "SYS_409"
    assert data["errorMessage"] == ("El correo electrónico ya está registrado")
    assert "userError" in data
    assert "info" in data


def test_get_current_user(authenticated_client):
    response = authenticated_client.get(
        "/users/me",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Usuario obtenido correctamente"

    assert data["data"]["name"] == "Fernando"
    assert data["data"]["email"] == "fernando@axity.com"


def test_get_users(authenticated_client):
    response = authenticated_client.get(
        "/users/",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Usuarios obtenidos correctamente"

    assert isinstance(data["data"], list)
    assert len(data["data"]) == 1

    assert data["data"][0]["name"] == "Fernando"


def test_get_user(authenticated_client):
    response = authenticated_client.get(
        "/users/1",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["id"] == 1
    assert data["data"]["name"] == "Fernando"


def test_get_user_not_found(authenticated_client):
    response = authenticated_client.get(
        "/users/999",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["errorCode"] == "SYS_404"
    assert data["errorMessage"] == "Usuario no encontrado"
    assert data["userError"] == ("No se encontró el recurso solicitado")
    assert data["info"] == "http://help.com"


def test_update_user(authenticated_client):
    response = authenticated_client.put(
        "/users/1",
        json={
            "name": "Fernando Actualizado",
            "email": "fernando.actualizado@axity.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Usuario actualizado correctamente"

    assert data["data"]["name"] == "Fernando Actualizado"
    assert data["data"]["email"] == ("fernando.actualizado@axity.com")


def test_delete_user(authenticated_client):
    response = authenticated_client.delete(
        "/users/1",
    )

    assert response.status_code == 204

    response = authenticated_client.get(
        "/users/1",
    )

    assert response.status_code == 401
