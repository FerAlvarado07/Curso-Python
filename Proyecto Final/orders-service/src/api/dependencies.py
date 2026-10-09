from collections.abc import Generator

from fastapi import Depends

import httpx
from sqlalchemy.orm import Session

from src.application.use_cases.cancel_order import CancelOrderUseCase
from src.application.use_cases.create_order import CreateOrderUseCase
from src.application.use_cases.get_order import GetOrderUseCase
from src.application.use_cases.list_orders import ListOrdersUseCase
from src.application.use_cases.delete_order import DeleteOrderUseCase
from src.domain.ports.notification import OrderNotification
from src.domain.ports.order_repository import OrderRepository
from src.infrastructure.database.session import SessionFactory
from src.infrastructure.database.sqlalchemy_order_repository import (
    SqlAlchemyOrderRepository,
)
from src.infrastructure.http.notification_adapter import (
    ConsoleNotificationAdapter,
    HttpNotificationAdapter,
)


from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.login_user import LoginUserUseCase
from src.domain.ports.user_repository import UserRepository
from src.infrastructure.database.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


def get_session() -> Generator[Session, None, None]:
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()


def get_order_repository(
    session: Session = Depends(get_session),
) -> OrderRepository:
    return SqlAlchemyOrderRepository(session)


def get_notification_adapter() -> Generator[OrderNotification, None, None]:
    from os import getenv

    notification_url = getenv("NOTIFICATION_URL")

    if not notification_url:
        yield ConsoleNotificationAdapter()
        return

    with httpx.Client(timeout=5.0) as client:
        yield HttpNotificationAdapter(client, notification_url)


def get_create_order_use_case(
    repository: OrderRepository = Depends(get_order_repository),
    notification: OrderNotification = Depends(get_notification_adapter),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(repository, notification)


def get_get_order_use_case(
    repository: OrderRepository = Depends(get_order_repository),
) -> GetOrderUseCase:
    return GetOrderUseCase(repository)


def get_list_orders_use_case(
    repository: OrderRepository = Depends(get_order_repository),
) -> ListOrdersUseCase:
    return ListOrdersUseCase(repository)


def get_cancel_order_use_case(
    repository: OrderRepository = Depends(get_order_repository),
) -> CancelOrderUseCase:
    return CancelOrderUseCase(repository)


def get_delete_order_use_case(
    repository: OrderRepository = Depends(get_order_repository),
) -> DeleteOrderUseCase:
    return DeleteOrderUseCase(repository)


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def get_register_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(repository)


def get_login_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
) -> LoginUserUseCase:
    return LoginUserUseCase(repository)
