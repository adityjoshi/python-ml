from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "http:///./greencart.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread"=True}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoFlush=True,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

