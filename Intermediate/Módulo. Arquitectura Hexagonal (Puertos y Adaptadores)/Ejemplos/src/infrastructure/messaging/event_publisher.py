from src.domain.entities.order import Order


class EventPublisher:
    """Adapter encargado de publicar eventos."""

    def publish_order_created(self, order: Order) -> None:
        """Publica un evento de orden creada."""

        print(f"Event published: order.created order_id={order.id}")
