from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError

from schemas.models import Bot


def get_token(authorization) -> str:
    token = authorization[len("Bearer "):]
    return token

def get_user_id_from_header(authorization: str) -> int:
    token = get_token(authorization)
    user_id = decode_access_token(token).get("user_id")
    return user_id


def get_tel_id_from_header(authorization: str) -> int:
    token = get_token(authorization)
    tel_id = decode_access_token(token).get("tel_id")
    return tel_id


def is_bot_owner(authorization: str, bot: Bot):
    if bot.user_id != get_user_id_from_header(authorization):
        raise HTTPException(status_code=400, detail="Bot doesn't belong to user")


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def refresh_token(authorization: str) -> str:
    token = authorization[len("Bearer "):]
    decoded_token = decode_access_token(token)
    new_token = create_access_token(decoded_token)
    return new_token

def verify_token(request: Request):
    excluded_paths = ["/login/", "/is-login-approved/", "/telebot-auth-accepted", "/refresh-token", "/get-image"]
    for path in excluded_paths:
        if request.url.path.startswith(path):
            return

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = get_token(auth_header)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")