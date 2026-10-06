from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.database import get_session
from src.dependencies import get_current_user
from src.models.order import Order
from src.models.user import User
from src.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)
from src.schemas.response import SuccessResponse
from src.services.order_service import (
    create_order,
    delete_order,
    get_order,
    get_order_total,
    get_orders,
    update_order,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def order_to_response(order: Order) -> dict:
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "items": [
            {
                "id": item.id,
                "product": item.product,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.subtotal,
            }
            for item in order.items
        ],
        "total": get_order_total(order),
    }


@router.post(
    "/",
    response_model=SuccessResponse[OrderResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_order_endpoint(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[OrderResponse]:
    order = create_order(
        session=session,
        user_id=current_user.id,
        order_data=order_data,
    )

    return SuccessResponse(
        message="Orden creada correctamente",
        data=order_to_response(order),
    )


@router.get(
    "/",
    response_model=SuccessResponse[list[OrderResponse]],
)
def get_orders_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[OrderResponse]]:
    orders = get_orders(
        session=session,
        user_id=current_user.id,
    )

    data = [order_to_response(order) for order in orders]

    return SuccessResponse(
        message="Órdenes obtenidas correctamente",
        data=data,
    )


@router.get(
    "/{order_id}",
    response_model=SuccessResponse[OrderResponse],
)
def get_order_endpoint(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[OrderResponse]:
    order = get_order(
        session=session,
        order_id=order_id,
        user_id=current_user.id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return SuccessResponse(
        message="Orden obtenida correctamente",
        data=order_to_response(order),
    )


@router.put(
    "/{order_id}",
    response_model=SuccessResponse[OrderResponse],
)
def update_order_endpoint(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[OrderResponse]:
    order = get_order(
        session=session,
        order_id=order_id,
        user_id=current_user.id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    order = update_order(
        session=session,
        order=order,
        order_data=order_data,
    )

    return SuccessResponse(
        message="Orden actualizada correctamente",
        data=order_to_response(order),
    )


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order_endpoint(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    order = get_order(
        session=session,
        order_id=order_id,
        user_id=current_user.id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    delete_order(
        session=session,
        order=order,
    )

    return SuccessResponse(
        message="Orden eliminada correctamente",
        data=order_to_response(order),
    )
