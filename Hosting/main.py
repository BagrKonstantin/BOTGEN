import asyncio
import logging
from asyncio.log import logger
from contextlib import asynccontextmanager
from datetime import datetime

import telebot.asyncio_helper
from fastapi import FastAPI, HTTPException

from graph.AbstractBot import AbstractBot
from services.sender_service import AsyncRabbitSender
from utils.config import session
from utils.models import Bot, Subscription
import traceback

running_bots: dict[int, asyncio.Task] = {}

sender = AsyncRabbitSender()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


def bot_crashed(task: asyncio.Task):
    try:
        task.result()
    except Exception:
        bot_id = int(task.get_name())
        running_bots.pop(bot_id)
        bot: Bot = session.query(Bot).filter(Bot.bot_id == bot_id).one_or_none()
        bot.is_launched = False
        session.commit()


async def run_bot(bot: Bot) -> None:
    try:
        bot_instance = AbstractBot(bot, sender)
        await bot_instance.try_token()
    except telebot.asyncio_helper.ApiException:
        raise RuntimeError("Bot token is invalid")
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(str(e))
    task = asyncio.create_task(bot_instance.run(), name=str(bot_instance.bot_id))
    task.add_done_callback(bot_crashed)
    running_bots[bot.bot_id] = task


@asynccontextmanager
async def lifespan(fastapp: FastAPI):
    try:
        bots = session.query(Bot).filter(Bot.is_launched == True).all()
        for bot in bots:
            subscription = session.query(Subscription).filter(Subscription.user_id == bot.user_id).one_or_none()
            if subscription is not None:
                if subscription.expiration_date >= datetime.today():
                    await run_bot(bot)
    except Exception as e:
        logger.error(e)
    await sender.connect()
    yield
    for task in running_bots.values():
        task.cancel()
        await task

app = FastAPI(lifespan=lifespan)




@app.post("/launch/{bot_id}")
async def launch_bot(bot_id: int):
    print(bot_id)
    bot: Bot = session.query(Bot).filter(Bot.bot_id == bot_id).one_or_none()
    if not bot.is_launched:
        try:
            await run_bot(bot)
            bot.is_launched = True
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        task = running_bots.pop(bot_id)
        task.cancel()
        await task
        bot.is_launched = False
    session.commit()
    return {"message": "Deployed" if bot.is_launched == True else "Stopped"}



