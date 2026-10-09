from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.domain.entities.order import Order
from src.infrastructure.database.memory_order_repository import (
    MemoryOrderRepository,
)
from src.infrastructure.database.sqlalchemy_order_repository import (
    Base,
    SQLAlchemyOrderRepository,
)


@pytest.fixture
def sqlalchemy_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    engine.dispose()


@pytest.fixture(
    params=["memory", "sqlalchemy"],
    ids=["memory-repository", "sqlalchemy-repository"],
)
def repository(request, sqlalchemy_session):
    if request.param == "memory":
        return MemoryOrderRepository()

    return SQLAlchemyOrderRepository(sqlalchemy_session)


def test_repository_can_save_and_find_order(repository) -> None:
    order = Order(
        id=uuid4(),
        customer_name="Alex",
        product="Keyboard",
        amount=1200,
        status="PENDING",
    )

    saved_order = repository.save(order)
    found_order = repository.find_by_id(order.id)

    assert saved_order.id == order.id
    assert found_order is not None
    assert found_order.id == order.id
    assert found_order.customer_name == "Alex"
    assert found_order.product == "Keyboard"
    assert found_order.amount == 1200
    assert found_order.status == "PENDING"


def test_repository_returns_none_for_missing_order(repository) -> None:
    result = repository.find_by_id(uuid4())

    assert result is None
