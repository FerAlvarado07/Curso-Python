from fastapi import Header, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.services.auth_service import decode_access_token
from src.services.user_service import get_user_by_id


def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> str:
    """
    Valida una API Key enviada mediante el header X-API-Key.
    """

    expected_api_key = "curso-python"

    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida",
        )

    return x_api_key


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict:
    """
    Obtiene el usuario asociado al JWT.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = get_user_by_id(
            int(user_id),
        )

        if user is None:
            raise credentials_exception

        return user

    except Exception as error:
        if isinstance(error, HTTPException):
            raise error

        raise credentials_exception from error
