from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from sqlalchemy.orm import Session

from src.database import get_session
from src.models.user import User
from src.services.auth_service import decode_access_token
from src.services.user_service import get_user_by_id

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = get_user_by_id(
            session,
            int(user_id),
        )

        if user is None:
            raise credentials_exception

        return user

    except (
        jwt.PyJWTError,
        ValueError,
        TypeError,
    ):
        raise credentials_exception
