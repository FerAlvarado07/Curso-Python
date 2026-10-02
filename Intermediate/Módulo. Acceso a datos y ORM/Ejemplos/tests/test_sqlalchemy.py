from sqlalchemy import create_engine

from src.sqlalchemy_orm_example import (
    Base,
    create_user,
    get_user,
    get_users,
)


def test_create_user():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    # Reemplazamos temporalmente el engine
    import src.sqlalchemy_orm_example as module

    original_engine = module.engine
    module.engine = engine

    try:
        create_user(
            "Fernando",
            "fernando@example.com",
        )

        user = get_user(1)

        assert user is not None
        assert user.name == "Fernando"
        assert user.email == "fernando@example.com"

    finally:
        module.engine = original_engine


def test_get_users():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    import src.sqlalchemy_orm_example as module

    original_engine = module.engine
    module.engine = engine

    try:
        create_user(
            "Fernando",
            "fernando@example.com",
        )

        create_user(
            "Ana",
            "ana@example.com",
        )

        users = get_users()

        assert len(users) == 2
        assert users[0].name == "Fernando"
        assert users[1].name == "Ana"

    finally:
        module.engine = original_engine
