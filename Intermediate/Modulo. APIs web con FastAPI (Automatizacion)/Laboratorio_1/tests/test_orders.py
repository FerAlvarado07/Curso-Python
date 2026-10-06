def test_create_order(authenticated_client):
    response = authenticated_client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product": "Teclado mecánico",
                    "quantity": 2,
                    "price": 1500.00,
                },
                {
                    "product": "Mouse",
                    "quantity": 1,
                    "price": 800.00,
                },
            ],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Orden creada correctamente"

    assert data["data"]["id"] == 1
    assert data["data"]["status"] == "pending"

    assert len(data["data"]["items"]) == 2

    assert data["data"]["items"][0]["product"] == ("Teclado mecánico")

    assert data["data"]["items"][0]["quantity"] == 2

    assert data["data"]["items"][1]["product"] == "Mouse"

    assert data["data"]["items"][1]["quantity"] == 1

    assert float(data["data"]["total"]) == 3800.00


def test_get_orders(authenticated_client):
    authenticated_client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product": "Laptop",
                    "quantity": 1,
                    "price": 25000,
                },
            ],
        },
    )

    response = authenticated_client.get(
        "/orders/",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Órdenes obtenidas correctamente"

    assert isinstance(data["data"], list)
    assert len(data["data"]) == 1

    assert data["data"][0]["items"][0]["product"] == "Laptop"


def test_get_order(authenticated_client):
    create_response = authenticated_client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product": "Monitor",
                    "quantity": 1,
                    "price": 5000,
                },
            ],
        },
    )

    order_id = create_response.json()["data"]["id"]

    response = authenticated_client.get(
        f"/orders/{order_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Orden obtenida correctamente"
    assert data["data"]["id"] == order_id

    assert data["data"]["items"][0]["product"] == "Monitor"


def test_get_order_not_found(authenticated_client):
    response = authenticated_client.get(
        "/orders/99999",
    )

    assert response.status_code == 404

    data = response.json()

    assert data["errorCode"] == "SYS_404"
    assert data["errorMessage"] == "Orden no encontrada"
    assert data["userError"] == ("No se encontró el recurso solicitado")


def test_update_order(authenticated_client):
    create_response = authenticated_client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product": "Teclado",
                    "quantity": 1,
                    "price": 1000,
                },
            ],
        },
    )

    order_id = create_response.json()["data"]["id"]

    response = authenticated_client.put(
        f"/orders/{order_id}",
        json={
            "status": "completed",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Orden actualizada correctamente"
    assert data["data"]["status"] == "completed"


def test_delete_order(authenticated_client):
    create_response = authenticated_client.post(
        "/orders/",
        json={
            "items": [
                {
                    "product": "Mouse",
                    "quantity": 1,
                    "price": 500,
                },
            ],
        },
    )

    order_id = create_response.json()["data"]["id"]

    response = authenticated_client.delete(
        f"/orders/{order_id}",
    )

    assert response.status_code == 204

    response = authenticated_client.get(
        f"/orders/{order_id}",
    )

    assert response.status_code == 404
