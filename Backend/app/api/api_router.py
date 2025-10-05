from fastapi import APIRouter
from app.api.v1.routes import posts, auth, files, projects

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/v1/posts", tags=["Posts"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
api_router.include_router(files.router, prefix="/v1/files", tags=["Files", "Images"])
api_router.include_router(projects.router, prefix="/v1/projects", tags=["Projects"])