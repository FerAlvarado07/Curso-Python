import os
from collections.abc import Iterator

from sqlalchemy.orm import Session

from src.application.use_cases.create_order import CreateOrder
from src.domain.ports.notification import OrderNotification
from src.domain.ports.order_repository import OrderRepository
from src.infrastructure.database.memory_order_repository import (
    MemoryOrderRepository,
)
from src.infrastructure.database.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
    create_database,
)
from src.infrastructure.http.notification_adapter import (
    HttpNotificationAdapter,
    create_simulated_http_client,
)

REPOSITORY_TYPE = os.getenv("ORDER_REPOSITORY", "memory")

memory_repository = MemoryOrderRepository()

engine = None

if REPOSITORY_TYPE == "sqlalchemy":
    engine = create_database(os.getenv("DATABASE_URL", "sqlite:///orders.db"))


def get_order_repository() -> Iterator[OrderRepository]:
    if REPOSITORY_TYPE == "memory":
        yield memory_repository
        return

    if REPOSITORY_TYPE == "sqlalchemy":
        if engine is None:
            raise RuntimeError("Database engine is not configured")

        with Session(engine) as session:
            yield SQLAlchemyOrderRepository(session)

        return

    raise RuntimeError(f"Unsupported repository type: {REPOSITORY_TYPE}")


def get_notification_adapter() -> Iterator[OrderNotification]:
    # El cliente simulado
    with create_simulated_http_client() as client:
        yield HttpNotificationAdapter(
            base_url="https://notifications.example.test",
            client=client,
        )


def get_create_order_use_case(
    repository: OrderRepository,
    notification: OrderNotification,
) -> CreateOrder:
    return CreateOrder(
        repository=repository,
        notification=notification,
    )
