from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_path = r"..\Backend\db\local_nasa_spaceapps.db"

DATABASE_URL = f"sqlite:///{db_path}"

def create_db(db_url: str = DATABASE_URL):
    print("Creating Database...")
    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()

    print("Creating Tables...")

    Base.metadata.create_all(bind=engine)

    print("Done! =D")

    return engine, SessionLocal, Base