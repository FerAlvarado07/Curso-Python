from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas.auth import Token
from src.schemas.response import SuccessResponse
from src.services.auth_service import (
    create_access_token,
    verify_password,
)
from src.services.user_service import get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=SuccessResponse[Token],
    summary="Iniciar sesión",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> SuccessResponse[Token]:
    user = get_user_by_email(
        session,
        form_data.username,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    password_valid = verify_password(
        form_data.password,
        user.password_hash,
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    token = Token(
        access_token=access_token,
        token_type="bearer",
    )

    return SuccessResponse(
        message="Inicio de sesión exitoso",
        data=token,
    )
