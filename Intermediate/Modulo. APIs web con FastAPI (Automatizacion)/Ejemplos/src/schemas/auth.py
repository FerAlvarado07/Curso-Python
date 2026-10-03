from pydantic import BaseModel


class Token(BaseModel):
    """
    Respuesta generada después de un login exitoso.
    """

    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """
    Datos utilizados para iniciar sesión.
    """

    email: str
    password: str
