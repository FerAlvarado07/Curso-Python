from decimal import Decimal

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product: str = Field(
        min_length=1,
        max_length=150,
        description="Nombre del producto",
        examples=["Teclado mecánico"],
    )

    quantity: int = Field(
        gt=0,
        description="Cantidad de productos",
        examples=[2],
    )

    price: Decimal = Field(
        gt=0,
        decimal_places=2,
        description="Precio unitario",
        examples=[1500.00],
    )


class OrderItemResponse(BaseModel):
    id: int
    product: str
    quantity: int
    price: Decimal
    subtotal: Decimal

    model_config = {
        "from_attributes": True,
    }


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(
        min_length=1,
        description="Productos de la orden",
    )


class OrderUpdate(BaseModel):
    status: str = Field(
        min_length=1,
        max_length=20,
        examples=["completed"],
    )


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    items: list[OrderItemResponse]
    total: Decimal

    model_config = {
        "from_attributes": True,
    }
