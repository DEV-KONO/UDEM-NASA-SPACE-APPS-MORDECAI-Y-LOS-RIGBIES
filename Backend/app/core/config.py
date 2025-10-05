from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_ENGINE: str
    DB_USER: str
    DB_PASS: str
    DB_IP: str
    DB_PORT: str
    DB_TABLENAME: str

    class Config:
        env_file = ".env"

settings = Settings()