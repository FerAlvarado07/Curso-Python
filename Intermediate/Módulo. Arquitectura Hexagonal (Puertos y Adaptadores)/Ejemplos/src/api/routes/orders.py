from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.dependencies import get_create_order_use_case
from src.application.dtos.order_dto import CreateOrderRequest
from src.application.use_cases.create_order import CreateOrderUseCase

router = APIRouter(prefix="/orders", tags=["Orders"])


class CreateOrderRequestModel(BaseModel):
    """Modelo HTTP utilizado para recibir la petición."""

    customer_name: str
    product: str
    amount: float


class OrderResponseModel(BaseModel):
    """Modelo HTTP utilizado para responder."""

    id: str
    customer_name: str
    product: str
    amount: float
    status: str


@router.post(
    "",
    response_model=OrderResponseModel,
)
def create_order(
    request: CreateOrderRequestModel,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
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
