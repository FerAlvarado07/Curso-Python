from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """
    Datos necesarios para crear un usuario.
    """

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100,
    )


class UserUpdate(BaseModel):
    """
    Datos necesarios para actualizar un usuario.
    """

    name: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr


class UserResponse(BaseModel):
    """
    Usuario que devuelve la API.
    """

    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )
