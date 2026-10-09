from uuid import UUID

from src.domain.ports.order_repository import OrderRepository


class DeleteOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: UUID) -> bool:
        return self.order_repository.delete(order_id)
