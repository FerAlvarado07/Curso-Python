from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session
