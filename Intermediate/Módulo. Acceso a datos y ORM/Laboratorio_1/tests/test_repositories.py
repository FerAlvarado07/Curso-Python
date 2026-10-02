from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base
from src.repository import (
    create_order,
    create_user,
    delete_order,
    delete_user,
    get_order,
    get_order_total,
    get_orders,
    get_user,
    get_users,
    update_user,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


def test_create_user(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    assert user.id is not None
    assert user.name == "Fernando"
    assert user.email == "fernando@example.com"


def test_get_user(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    result = get_user(
        session,
        user.id,
    )

    assert result is not None
    assert result.name == "Fernando"


def test_get_users(session):
    create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    create_user(
        session,
        "Ana",
        "ana@example.com",
    )

    users = get_users(session)

    assert len(users) == 2
    assert users[0].name == "Fernando"
    assert users[1].name == "Ana"


def test_update_user(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    updated_user = update_user(
        session,
        user.id,
        "Fernando Enrique",
        "fernando.enrique@example.com",
    )

    assert updated_user is not None
    assert updated_user.name == "Fernando Enrique"
    assert updated_user.email == "fernando.enrique@example.com"


def test_delete_user(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    result = delete_user(
        session,
        user.id,
    )

    assert result is True
    assert get_user(session, user.id) is None


def test_create_order(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    order = create_order(
        session,
        user.id,
        [
            {
                "product": "Teclado",
                "quantity": 1,
                "price": 850,
            },
            {
                "product": "Mouse",
                "quantity": 2,
                "price": 450,
            },
        ],
    )

    assert order.id is not None
    assert order.user_id == user.id

    assert len(order.items) == 2
    assert order.items[0].product == "Teclado"
    assert order.items[1].product == "Mouse"


def test_get_order(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    order = create_order(
        session,
        user.id,
        [
            {
                "product": "Monitor",
                "quantity": 1,
                "price": 5000,
            },
        ],
    )

    result = get_order(
        session,
        order.id,
    )

    assert result is not None
    assert len(result.items) == 1
    assert result.items[0].product == "Monitor"


def test_order_total(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    order = create_order(
        session,
        user.id,
        [
            {
                "product": "Teclado",
                "quantity": 1,
                "price": 850,
            },
            {
                "product": "Mouse",
                "quantity": 2,
                "price": 450,
            },
        ],
    )

    total = get_order_total(order)

    assert total == Decimal("1750")


def test_get_orders(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    create_order(
        session,
        user.id,
        [
            {
                "product": "Teclado",
                "quantity": 1,
                "price": 850,
            },
        ],
    )

    create_order(
        session,
        user.id,
        [
            {
                "product": "Mouse",
                "quantity": 1,
                "price": 450,
            },
        ],
    )

    orders = get_orders(session)

    assert len(orders) == 2


def test_delete_order(session):
    user = create_user(
        session,
        "Fernando",
        "fernando@example.com",
    )

    order = create_order(
        session,
        user.id,
        [
            {
                "product": "Teclado",
                "quantity": 1,
                "price": 850,
            },
        ],
    )

    result = delete_order(
        session,
        order.id,
    )

    assert result is True
    assert get_order(session, order.id) is None
