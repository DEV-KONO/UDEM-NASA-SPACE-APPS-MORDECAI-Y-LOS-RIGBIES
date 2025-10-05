from os import getenv
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

db_url = getenv('DB_URL')

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)

base = declarative_base()

def get_db():
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()