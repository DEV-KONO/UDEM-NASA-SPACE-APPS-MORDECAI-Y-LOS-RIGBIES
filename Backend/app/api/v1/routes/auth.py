from datetime import timedelta
from os import getenv
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.db.models.users import Users
from app.crud.user import create_access_token, verify_access_token, verify_password
from sqlalchemy.orm import Session

load_dotenv()

router = APIRouter()

@router.post("/login")
def login(response: Response,form_data: OAuth2PasswordRequestForm = Depends(), session = Depends(get_db)):
    user = session.query(Users).filter(Users.username == form_data.username).one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales Incorrectas")
    
    access_token_expires = timedelta(minutes=int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60*int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
    )

    return {"msg": "Login satisfactory =D"}

@router.get("/check")
def check_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No token")

    payload = verify_access_token(token=token, db=db)

    return {"message": f"User checked! =D, username: {payload['sub']}"}