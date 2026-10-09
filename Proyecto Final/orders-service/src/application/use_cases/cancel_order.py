from uuid import UUID

from src.application.dtos.order_dto import OrderResponseDTO
from src.domain.exceptions.order_exceptions import OrderNotFoundError
from src.domain.ports.order_repository import OrderRepository


class CancelOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def execute(self, order_id: UUID) -> OrderResponseDTO:
        order = self._repository.find_by_id(order_id)

        if order is None:
            raise OrderNotFoundError(
                f"No existe la orden con identificador {order_id}."
            )

        order.cancel()
        saved_order = self._repository.save(order)

        return OrderResponseDTO.from_entity(saved_order)
