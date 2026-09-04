
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./fleettrack.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_threads": False}

)

SessionLocal = sessionmaker(
    autoflush=True,
    autocommit=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal
    try:
        yield db

    finally:
        db.close()
