import json
import logging
from io import BytesIO
from typing import Any, Dict

from fastapi import APIRouter, Header, UploadFile, File, Request
from fastapi.responses import JSONResponse, StreamingResponse

from service.auth_service import is_bot_owner, get_user_id_from_header, get_tel_id_from_header
from service.bot_service import *
from utils.bot import BotSettings
from utils.models import Bot

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.post("/new-bot/{token}")
async def new_bot_endpoint(token: str, request: Request, authorization: str = Header(None)):
    user_id = get_user_id_from_header(authorization)
    data = await request.json()
    bot = await new_bot(user_id, token, data)
    return bot


@router.post("/save-bot/{bot_id}")
async def save_bot_endpoint(bot_id: int, dialogs: Dict[Any, Any], authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    await save_bot(bot, dialogs)


@router.get("/all-bots")
async def get_all_bots_endpoint(authorization: str = Header(None)):
    user_id = get_user_id_from_header(authorization)

    bots = await get_all_bots(user_id)
    return bots


@router.get("/get-bot/{bot_id}")
async def get_bot_by_id(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    data = json.loads(bot.data_json)
    return JSONResponse(content=data)


@router.delete("/delete-bot/{bot_id}")
async def delete_bot_endpoint(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    await delete_bot(bot)


@router.post("/launch-bot/{bot_id}")
async def launch_bot_endpoint(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    bot: Bot = await launch_bot(bot)
    return bot


@router.post("/upload-image/{bot_id}")
async def upload_image(bot_id: int, image: UploadFile = File(...), authorization: str = Header(None)):
    tel_id = get_tel_id_from_header(authorization)
    contents = await image.read()
    bot = await get_bot(bot_id)
    image_id = telegram_service.send_image(tel_id, bot.token, contents)

    return {"image_id": image_id}


@router.get("/get-image/{bot_id}/{image_id}")
async def get_image(bot_id: int, image_id: str):
    bot = await get_bot(bot_id)
    image: bytes = telegram_service.get_image(bot.token, image_id)
    return StreamingResponse(BytesIO(image), media_type="image/jpeg")


@router.get("/get-bot-settings/{bot_id}")
async def get_bot_settings_endpoint(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    bot_setting: BotSettings = await get_bot_settings(bot)
    return bot_setting


@router.post("/save-settings/{bot_id}")
async def save_settings_endpoint(bot_id: int, settings: BotSettings, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    await save_settings(bot, settings)
