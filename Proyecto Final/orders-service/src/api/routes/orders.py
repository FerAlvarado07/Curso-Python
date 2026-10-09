from collections.abc import Generator
from http.client import HTTPException
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies import (
    get_cancel_order_use_case,
    get_create_order_use_case,
    get_get_order_use_case,
    get_list_orders_use_case,
    get_delete_order_use_case,
    get_notification_adapter,
    get_order_repository,
    get_session,
)
from src.api.schemas.order_schema import (
    CreateOrderRequest,
    OrderListResponse,
    OrderResponse,
)
from src.application.dtos.order_dto import CreateOrderDTO
from src.application.use_cases.cancel_order import CancelOrderUseCase
from src.application.use_cases.create_order import CreateOrderUseCase
from src.application.use_cases.get_order import GetOrderUseCase
from src.application.use_cases.list_orders import ListOrdersUseCase
from src.application.use_cases.delete_order import DeleteOrderUseCase
from src.domain.ports.notification import OrderNotification
from src.domain.ports.order_repository import OrderRepository
from src.infrastructure.security.current_user import get_current_user

order_router = APIRouter(
    prefix="/order",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)],
)

orders_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_user)],
)


def repository_dependency(
    session: Annotated[Session, Depends(get_session)],
) -> OrderRepository:
    return get_order_repository(session)


def notification_dependency() -> Generator[OrderNotification, None, None]:
    yield from get_notification_adapter()


@order_router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una orden",
)
def create_order(
    request: CreateOrderRequest,
    repository: Annotated[OrderRepository, Depends(repository_dependency)],
    notification: Annotated[
        OrderNotification,
        Depends(notification_dependency),
    ],
) -> OrderResponse:
    use_case: CreateOrderUseCase = get_create_order_use_case(
        repository,
        notification,
    )

    result = use_case.execute(
        CreateOrderDTO(
            customer_id=request.customer_id,
            amount=request.amount,
            currency=request.currency,
        )
    )

    return OrderResponse.model_validate(result)


@orders_router.get(
    "",
    response_model=OrderListResponse,
    summary="Listar órdenes",
)
def list_orders(
    repository: Annotated[OrderRepository, Depends(repository_dependency)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> OrderListResponse:
    use_case: ListOrdersUseCase = get_list_orders_use_case(repository)
    result = use_case.execute(offset=offset, limit=limit)

    return OrderListResponse.model_validate(result)


@order_router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Obtener una orden",
)
def get_order(
    order_id: UUID,
    repository: Annotated[OrderRepository, Depends(repository_dependency)],
) -> OrderResponse:
    use_case: GetOrderUseCase = get_get_order_use_case(repository)
    result = use_case.execute(order_id)

    return OrderResponse.model_validate(result)


@orders_router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
    summary="Cancelar una orden",
)
def cancel_order(
    order_id: UUID,
    repository: Annotated[OrderRepository, Depends(repository_dependency)],
) -> OrderResponse:
    use_case: CancelOrderUseCase = get_cancel_order_use_case(repository)
    result = use_case.execute(order_id)

    return OrderResponse.model_validate(result)


@order_router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una orden",
)
def delete_order(
    order_id: UUID,
    use_case: Annotated[
        DeleteOrderUseCase,
        Depends(get_delete_order_use_case),
    ],
) -> None:
    deleted = use_case.execute(order_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order no encontrada",
        )
