from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.order import OrderStatus


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=100)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(
        default="MXN",
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
    )


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: str
    amount: Decimal
    currency: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class OrderListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[OrderResponse]
    total: int
    offset: int
    limit: int


class PingResponse(BaseModel):
    status: Literal["pong"]
