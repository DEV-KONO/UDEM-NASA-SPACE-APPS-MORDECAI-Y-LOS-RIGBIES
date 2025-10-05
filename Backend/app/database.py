from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy import event
from os import path
from datetime import datetime

# SQLite file path (relative to project root)
DATABASE_FILE = "leo_kickstarter.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Create engine with check_same_thread disabled for SQLite + SQLAlchemy
engine: Engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory for DB interactions
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Declarative base for models to inherit from
Base = declarative_base()


def get_db():
    """Yield a database session, ensuring it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ensure foreign key constraints are enforced in SQLite
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        pass
