from fastapi import FastAPI
from app.utils import init_db
from app.routes import router

app = FastAPI(title="LaunchLabs backend for the NASA Space Apps Hackathon")

app.include_router(router)

init_db()

@app.get("/")
def root():
    return {"message":"Healthy (●'◡'●)"}
