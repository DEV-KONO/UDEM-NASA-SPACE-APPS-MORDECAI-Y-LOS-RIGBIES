from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from app.api.api_router import api_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

origins = [
    "https://devjourney.software"
]

app = FastAPI()

app.include_router(api_router, prefix="/api")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)