from src.application.dtos.order_dto import OrderListDTO, OrderResponseDTO
from src.domain.ports.order_repository import OrderRepository


class ListOrdersUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def execute(self, offset: int = 0, limit: int = 20) -> OrderListDTO:
        orders = self._repository.list_orders(offset=offset, limit=limit)
        total = self._repository.count()

        return OrderListDTO(
            items=[OrderResponseDTO.from_entity(order) for order in orders],
            total=total,
            offset=offset,
            limit=limit,
        )
