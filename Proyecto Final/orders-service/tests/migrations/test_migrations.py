import os
import subprocess

import pytest
from sqlalchemy import create_engine, inspect


def test_migrations_create_expected_tables():
    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")

    engine = create_engine(database_url, pool_pre_ping=True)

    try:
        existing_tables = set(inspect(engine).get_table_names())

        if existing_tables:
            pytest.fail("Migration test requires an empty, disposable database.")

        environment = os.environ.copy()
        environment["DATABASE_URL"] = database_url

        subprocess.run(
            ["poetry", "run", "alembic", "upgrade", "head"],
            check=True,
            env=environment,
            capture_output=True,
            text=True,
        )

        tables = set(inspect(engine).get_table_names())

        assert "orders" in tables
        assert "users" in tables

    finally:
        engine.dispose()
