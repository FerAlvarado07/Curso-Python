import logging
import os

import httpx

from src.domain.entities.order import Order
from src.domain.exceptions.order_exceptions import NotificationError
from src.domain.ports.notification import OrderNotification

logger = logging.getLogger(__name__)


class HttpNotificationAdapter(OrderNotification):
    def __init__(
        self,
        client: httpx.Client,
        notification_url: str,
    ) -> None:
        self._client = client
        self._notification_url = notification_url

    def send_order_created(self, order: Order) -> None:
        payload = {
            "event": "order.created",
            "order_id": str(order.id),
            "customer_id": order.customer_id,
            "amount": str(order.amount),
            "currency": order.currency,
        }

        try:
            response = self._client.post(
                self._notification_url,
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise NotificationError(
                "No fue posible enviar la notificación de la orden."
            ) from exc


class ConsoleNotificationAdapter(OrderNotification):
    def send_order_created(self, order: Order) -> None:
        logger.info(
            "Orden creada: id=%s customer_id=%s",
            order.id,
            order.customer_id,
        )


def create_notification_adapter() -> OrderNotification:
    notification_url = os.getenv("NOTIFICATION_URL")

    if not notification_url:
        return ConsoleNotificationAdapter()

    client = httpx.Client(timeout=5.0)
    return HttpNotificationAdapter(client, notification_url)
