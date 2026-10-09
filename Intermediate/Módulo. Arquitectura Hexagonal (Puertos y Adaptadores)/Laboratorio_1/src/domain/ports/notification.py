from typing import Protocol
from uuid import UUID


class OrderNotification(Protocol):
    def notify_order_created(
        self,
        order_id: UUID,
        customer_name: str,
    ) -> None: ...
