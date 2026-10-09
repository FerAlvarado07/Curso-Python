from typing import Protocol

from src.domain.entities.order import Order


class OrderNotification(Protocol):
    def send_order_created(self, order: Order) -> None: ...
