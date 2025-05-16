import json
import logging
from datetime import datetime
from typing import Dict, Any, Union

import requests
from fastapi import HTTPException
from requests import Response
from sqlalchemy import select

from service import telegram_service
from utils.bot import BotSettings, Notifications
from utils.config import session, HOSTING_URL
from utils.models import Bot, Subscription, User, ProductType

logger = logging.getLogger(__name__)


async def get_bot(bot_id: int) -> Bot:
    bot: Union[Bot, None] = await session.get(Bot, bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

async def new_bot(user_id: int, token:str, data: Dict[str, Any]) -> Bot:
    name = data.get("name")
    bot = Bot(
        user_id=user_id,
        name=name,
        token=token,
    )
    session.add(bot)
    await session.commit()

    return bot

async def get_all_bots(user_id: int):
    bots = (await session.scalars(select(Bot).where(Bot.user_id == user_id).order_by(Bot.bot_id))).all()
    logger.info(f"User {user_id} requested list of bots ({len(bots)})")
    return bots

async def delete_bot(bot: Bot):
    await session.delete(bot)
    await session.commit()



async def save_bot(bot: Bot, dialogs: Dict[Any, Any]):
    bot.data_json = json.dumps(dialogs)
    for dialog_key, dialog_value in dialogs["dialogs"].items():
        for stage_key, stage_value in dialog_value["stages"].items():
            if stage_value["type"] == "product":
                product = await session.scalar(
                    select(ProductType).where(ProductType.name == stage_value["product"]["title"]))
                if product is None:
                    session.add(ProductType(bot_id=bot.bot_id, name=stage_value["product"]["title"],
                                            price=stage_value["product"]["price"]))
                else:
                    product.price = stage_value["product"]["price"]
    logger.info(f"Bot {bot.bot_id} was saved successfully")
    await session.commit()


async def launch_bot(bot: Bot):
    subscription = await session.scalar(select(Subscription).where(Subscription.user_id == bot.user_id))
    if subscription is not None:
        if subscription.expiration_date >= datetime.today():
            response: Response = requests.post(
                url=HOSTING_URL + f"/launch/{bot.bot_id}",
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.json()["detail"])
            await session.refresh(bot)
            return bot
    user = await session.scalar(select(User).where(User.user_id == bot.user_id))
    telegram_service.send_payment(user.tel_id)
    raise HTTPException(status_code=403,
                        detail="Purchase subscription in @botgen_official_bot to be able to host your bots")


async def get_bot_settings(bot: Bot):
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


async def save_settings(bot: Bot, settings: BotSettings):
    bot.name = settings.name
    bot.token = settings.token
    bot.greeting_message = settings.greeting_message

    notifications: Notifications = settings.notifications
    bot.notify_on_sold = notifications.on_product_sold
    bot.notify_on_out_of_stock = notifications.on_out_of_stock
    bot.notify_on_new_user = notifications.on_new_user

    await session.commit()
