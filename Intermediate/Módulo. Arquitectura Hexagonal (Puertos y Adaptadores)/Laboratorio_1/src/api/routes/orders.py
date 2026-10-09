from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.api.dependencies import (
    get_create_order_use_case,
    get_notification_adapter,
    get_order_repository,
)
from src.application.use_cases.create_order import (
    CreateOrder,
    CreateOrderRequest,
)
from src.domain.ports.notification import OrderNotification
from src.domain.ports.order_repository import OrderRepository

router = APIRouter(prefix="/orders", tags=["Orders"])


class CreateOrderRequestModel(BaseModel):
    customer_name: str = Field(min_length=1, max_length=150)
    product: str = Field(min_length=1, max_length=150)
    amount: float = Field(gt=0)


class OrderResponseModel(BaseModel):
    id: str
    customer_name: str
    product: str
    amount: float
    status: str


def provide_create_order_use_case(
    repository: Annotated[
        OrderRepository,
        Depends(get_order_repository),
    ],
    notification: Annotated[
        OrderNotification,
        Depends(get_notification_adapter),
    ],
) -> CreateOrder:
    return get_create_order_use_case(
        repository=repository,
        notification=notification,
    )


@router.post("", response_model=OrderResponseModel, status_code=201)
def create_order(
    request: CreateOrderRequestModel,
    use_case: Annotated[
        CreateOrder,
        Depends(provide_create_order_use_case),
    ],
) -> OrderResponseModel:
    try:
        result = use_case.execute(
            CreateOrderRequest(
                customer_name=request.customer_name,
                product=request.product,
                amount=request.amount,
            )
        )

        return OrderResponseModel(
            id=str(result.id),
            customer_name=result.customer_name,
            product=result.product,
            amount=result.amount,
            status=result.status,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
