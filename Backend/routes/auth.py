import logging

from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import select

from service.auth_service import create_access_token, refresh_token
from service.telegram_service import send_auth_request
from utils.config import session
from utils.models import User

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)
users_dic = dict()


@router.post("/login/{username}")
async def request_login(username: str):
    username = username.lower()
    user = await session.scalar(select(User).where(User.username == username))
    if not user:
        logger.info(f"{username} was not found")
        raise HTTPException(status_code=404, detail="Use @botgen_official_bot to register")
    token = send_auth_request(user)
    logger.info("Temporal token was issued successfully")
    return {"token": token}


@router.get("/refresh-token")
async def refresh_token_endpoint(authorization: str = Header(None)):
    access_token = refresh_token(authorization)
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/is-login-approved/{token}")
async def is_login_approved(token: str):
    if token in users_dic:
        tel_id = users_dic.pop(token)
        user = await session.scalar(select(User).where(User.tel_id == tel_id))
        access_token = create_access_token({"user_id": user.user_id, "tel_id": user.tel_id, "username": user.username})

        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(status_code=401, detail="Unauthorized")
