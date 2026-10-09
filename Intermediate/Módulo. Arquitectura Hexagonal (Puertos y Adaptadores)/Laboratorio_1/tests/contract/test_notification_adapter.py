import json
from uuid import uuid4

import httpx

from src.infrastructure.http.notification_adapter import (
    HttpNotificationAdapter,
)


def test_notification_adapter_sends_expected_request() -> None:
    captured_requests: list[httpx.Request] = []

    def handle_request(
        request: httpx.Request,
    ) -> httpx.Response:
        captured_requests.append(request)

        return httpx.Response(
            status_code=202,
            json={"message": "Notificación aceptada"},
        )

    client = httpx.Client(transport=httpx.MockTransport(handle_request))

    try:
        adapter = HttpNotificationAdapter(
            base_url="https://notifications.example.test",
            client=client,
        )

        order_id = uuid4()

        adapter.notify_order_created(
            order_id=order_id,
            customer_name="Alex",
        )

        assert len(captured_requests) == 1

        request = captured_requests[0]

        assert request.method == "POST"
        assert str(request.url) == ("https://notifications.example.test/notifications")

        payload = json.loads(request.content)

        assert payload == {
            "event": "order.created",
            "order_id": str(order_id),
            "customer_name": "Alex",
        }
    finally:
        client.close()


def test_notification_adapter_raises_on_http_error() -> None:
    def handle_request(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(status_code=500)

    with httpx.Client(transport=httpx.MockTransport(handle_request)) as client:
        adapter = HttpNotificationAdapter(
            base_url="https://notifications.example.test",
            client=client,
        )

        try:
            adapter.notify_order_created(
                order_id=uuid4(),
                customer_name="Alex",
            )
        except httpx.HTTPStatusError:
            pass
        else:
            raise AssertionError("Expected an HTTPStatusError for status 500")
