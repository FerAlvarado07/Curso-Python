from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Base

DATABASE_URL = "sqlite:///orders.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


def create_database() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
