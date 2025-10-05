from datetime import timedelta, timezone
import datetime
from os import getenv
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.models.users import Users
from app.core.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + (expires_delta or timedelta(minutes=getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp":int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt

def verify_access_token(token: str, db: Session):
    try:
        # decode con verificación de expiración automática
        payload = jwt.decode(
            token,
            getenv("SECRET_KEY"),
            algorithms=[getenv("ALGORITHM")],
            options={"verify_exp": True}  # esto hace que se lance ExpiredSignatureError si caduca
        )

        username = payload.get("sub")

        user = db.query(Users).filter(Users.username == username).one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="User doesn't Exist! T_T")
        if not user.admin:
            raise HTTPException(status_code=403, detail="The user is not admin :P")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expirado")  # <--- 401 para expirado
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid JWT T_T")   # <--- 403 para inválido