from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="LaunchLabs backend for the NASA Space Apps Hackathon")

app.include_router(router)

@app.get("/")
def root():
    return {"message":"Healthy (●'◡'●)"}
