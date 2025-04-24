from fastapi import APIRouter, HTTPException, Response, Header
from sqlalchemy import select
import logging
from config import session
from services.auth_service import create_access_token, refresh_token
from services.bot_service import send_auth_request
from schemas.models import User


router = APIRouter()

users_dic = dict()



@router.post("/login/{username}")
async def request_login(username: str):
    logging.info(username)
    username = username.lower()
    user = await session.scalar(select(User).where(User.username == username))
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    token = send_auth_request(user)
    return {"token": token}

@router.get("/refresh-token")
async def refresh_token_endpoint(authorization: str = Header(None)):
    access_token = refresh_token(authorization)
    return {"access_token": access_token, "token_type": "Bearer"}

@router.get("/is-login-approved/{token}")
async def is_login_approved(token:str):
    if token in users_dic:
        tel_id = users_dic.pop(token)
        user = await session.scalar(select(User).where(User.tel_id == tel_id))
        access_token = create_access_token({"user_id": user.user_id, "tel_id": user.tel_id, "username": user.username})

        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(status_code=401, detail="Unauthorized")

