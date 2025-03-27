from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Tuple

import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from src.config.constants import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def get_current_user(token: str = Security(oauth2_scheme)):
    payload = decode_access_token(token)
    return payload.get("sub")

def create_tokens(data: dict) -> Tuple[str, str]:
    to_encode = data.copy()

    access_expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": access_expire, "type": "access"})
    access_token = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    
    refresh_expire = datetime.utcnow() + timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": refresh_expire, "type": "refresh"})
    refresh_token = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    
    return access_token, refresh_token

def decode_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        if payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail=f"Invalid token type, expected {token_type}")
        return payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def refresh_access_token(refresh_token: str) -> str:
    payload = decode_token(refresh_token, "refresh")
    
    new_access_token = jwt.encode(
        {"sub": payload["sub"], "type": "access"},
        Settings.SECRET_KEY,
        algorithm=Settings.ALGORITHM
    )
    
    return new_access_token
