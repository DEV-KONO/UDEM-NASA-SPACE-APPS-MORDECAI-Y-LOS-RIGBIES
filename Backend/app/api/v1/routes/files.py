import token
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
import os
from app.core.database import get_db
from app.crud.user import verify_access_token

from fastapi.responses import JSONResponse

router = APIRouter()

# Aqui se guardan las imagenes
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/image")
async def upload_image(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Checar token antes de subir la foto
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No tokens? :(")
    payload = verify_access_token(token=token, db=db)
    
    # extension del archivo
    ext = file.filename.split(".")[-1]

    # nombre unico
    file_name = f"{uuid4()}.{ext}"

    # path del archivo
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Guardar el archivo en disco
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    file_url = f"/uploads/{file_name}"

    return JSONResponse(content={"url": file_url})