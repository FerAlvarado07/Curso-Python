from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.database import get_session
from src.dependencies import get_current_user
from src.models.user import User
from src.schemas.response import SuccessResponse
from src.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from src.services.user_service import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user_endpoint(
    user_data: UserCreate,
    session: Session = Depends(get_session),
) -> SuccessResponse[UserResponse]:
    existing_user = get_user_by_email(
        session,
        str(user_data.email),
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado",
        )

    user = create_user(
        session,
        user_data,
    )

    return SuccessResponse(
        message="Usuario creado correctamente",
        data=user,
    )


@router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
)
def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
) -> SuccessResponse[UserResponse]:
    return SuccessResponse(
        message="Usuario obtenido correctamente",
        data=current_user,
    )


@router.get(
    "/",
    response_model=SuccessResponse[list[UserResponse]],
)
def get_users_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[list[UserResponse]]:
    users = get_all_users(session)

    return SuccessResponse(
        message="Usuarios obtenidos correctamente",
        data=users,
    )


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
)
def get_user_endpoint(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[UserResponse]:
    user = get_user_by_id(
        session,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return SuccessResponse(
        message="Usuario obtenido correctamente",
        data=user,
    )


@router.put(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> SuccessResponse[UserResponse]:
    user = get_user_by_id(
        session,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    existing_user = get_user_by_email(
        session,
        str(user_data.email),
    )

    if existing_user is not None and existing_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado",
        )

    user = update_user(
        session,
        user,
        user_data,
    )

    return SuccessResponse(
        message="Usuario actualizado correctamente",
        data=user,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_endpoint(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    user = get_user_by_id(
        session,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    delete_user(
        session,
        user,
    )
