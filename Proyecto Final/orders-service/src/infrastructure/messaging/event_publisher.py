from src.domain.entities.order import Order


class EventPublisher:
    def publish_order_created(self, order: Order) -> None:
        print(f"Evento publicado: order.created order_id={order.id}")
