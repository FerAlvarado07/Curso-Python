from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
)
from src.api.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from src.application.use_cases.login_user import (
    InvalidCredentialsError,
    LoginUserUseCase,
)
from src.application.use_cases.register_user import (
    EmailAlreadyRegisteredError,
    RegisterUserUseCase,
)
from src.infrastructure.security.jwt_service import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
) -> UserResponse:
    try:
        user = use_case.execute(
            email=str(request.email),
            password=request.password,
        )
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado.",
        ) from None

    return UserResponse.model_validate(user)


@auth_router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case),
) -> LoginResponse:
    try:
        user = use_case.execute(
            email=str(request.email),
            password=request.password,
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    token = create_access_token(user.id)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )
