import httpx
from uuid import UUID


class HttpNotificationAdapter:
    def __init__(
        self,
        base_url: str,
        client: httpx.Client,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client

    def notify_order_created(
        self,
        order_id: UUID,
        customer_name: str,
    ) -> None:
        response = self.client.post(
            f"{self.base_url}/notifications",
            json={
                "event": "order.created",
                "order_id": str(order_id),
                "customer_name": customer_name,
            },
        )

        response.raise_for_status()


def create_simulated_http_client() -> httpx.Client:
    def handle_request(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=202,
            json={"message": "Notificación aceptada"},
        )

    transport = httpx.MockTransport(handle_request)

    return httpx.Client(transport=transport)
