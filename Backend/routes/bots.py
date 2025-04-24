import json
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, Union
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Header, UploadFile, File, Request, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select

from schemas.bot import BotSettings, Notifications
from services import bot_service
from config import session, HOSTING_URL
from schemas.models import Bot, ProductType, Subscription, User
import requests
from services.auth_service import is_bot_owner, get_user_id_from_header, get_tel_id_from_header

router = APIRouter()

async def get_bot(bot_id: int) -> Bot:
    bot: Union[Bot, None] = await session.get(Bot, bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

@router.post("/new-bot/{token}")
async def new_bot(token: str, request: Request, authorization: str = Header(None)):
    user_id = get_user_id_from_header(authorization)
    data = await request.json()
    name = data.get("name")
    bot = Bot(
        user_id=user_id,
        name=name,
        token=token,
    )
    session.add(bot)
    await session.commit()
    return bot



@router.post("/save-bot/{bot_id}")
async def save_bot(bot_id: int, dialogs: Dict[Any, Any], authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)
    bot.data_json = json.dumps(dialogs)
    for dialog_key, dialog_value in dialogs["dialogs"].items():
        for stage_key, stage_value in dialog_value["stages"].items():
            if stage_value["type"] == "product":
                product = await session.scalar(select(ProductType).where(ProductType.name == stage_value["product"]["title"]))
                if product is None:
                    session.add(ProductType(bot_id=bot_id, name=stage_value["product"]["title"],
                                            price=stage_value["product"]["price"]))
                else:
                    product.price = stage_value["product"]["price"]
    await session.commit()







@router.get("/all-bots")
async def get_all_bots(authorization: str = Header(None)):
    user_id = get_user_id_from_header(authorization)
    bots = (await session.scalars(select(Bot).where(Bot.user_id == user_id).order_by(Bot.bot_id))).all()
    return bots


@router.get("/get-bot/{bot_id}")
async def get_bot_by_id(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    data = json.loads(bot.data_json)
    return JSONResponse(content=data)


@router.delete("/delete-bot/{bot_id}")
async def delete_bot(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    await session.delete(bot)
    await session.commit()


@router.post("/launch-bot/{bot_id}")
async def launch_bot(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    subscription = await session.scalar(select(Subscription).where(Subscription.user_id == bot.user_id))
    if subscription is not None:
        if subscription.expiration_date >= datetime.today():
            print(HOSTING_URL)
            response = requests.post(
                url=HOSTING_URL + f"/launch/{bot_id}",
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Something went wrong")
            session.expire(bot)
            await session.refresh(bot)
            return bot
    user = await session.scalar(select(User).where(User.user_id == bot.user_id))
    bot_service.send_payment(user.tel_id)
    return bot


@router.post("/upload-image/{bot_id}")
async def upload_image(bot_id: int, image: UploadFile = File(...), authorization: str = Header(None)):
    tel_id = get_tel_id_from_header(authorization)
    contents = await image.read()
    bot = await get_bot(bot_id)
    image_id = bot_service.send_image(tel_id, bot.token, contents)

    return {"image_id": image_id}


@router.get("/get-image/{bot_id}/{image_id}")
async def get_image(bot_id: int, image_id: str):
    bot = await get_bot(bot_id)
    image: bytes = bot_service.get_image(bot.token, image_id)
    return StreamingResponse(BytesIO(image), media_type="image/jpeg")


@router.get("/get-bot-settings/{bot_id}")
async def get_bot_settings(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    notifications: Notifications = Notifications(
        on_new_user=bot.notify_on_new_user,
        on_product_sold=bot.notify_on_sold,
        on_out_of_stock=bot.notify_on_out_of_stock
    )
    return BotSettings(
        name=bot.name,
        token=bot.token,
        greeting_message=bot.greeting_message,
        notifications=notifications
    )


@router.post("/save-settings/{bot_id}")
async def save_settings(bot_id: int, settings: BotSettings, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    bot.name = settings.name
    bot.token = settings.token
    bot.greeting_message = settings.greeting_message

    notifications: Notifications = settings.notifications
    bot.notify_on_sold = notifications.on_product_sold
    bot.notify_on_out_of_stock = notifications.on_out_of_stock
    bot.notify_on_new_user = notifications.on_new_user

    await session.commit()
