from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_current_user
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.services.user_service import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_endpoint(user_data: UserCreate) -> dict:
    return create_user(user_data)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    current_user: dict = Depends(get_current_user),
) -> list[dict]:
    return get_all_users()


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_data(
    current_user: dict = Depends(get_current_user),
) -> dict:
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
) -> dict:
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
) -> dict:
    user = update_user(user_id, user_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_endpoint(
    user_id: int,
    current_user: dict = Depends(get_current_user),
) -> None:
    deleted = delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
