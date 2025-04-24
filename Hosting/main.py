import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from threading import Thread
from graph.AbstractBot import AbstractBot
from utils.models import Bot
from utils.config import session
from services.sender_service import AsyncRabbitSender

running_bots: dict[int, asyncio.Task] = {}

sender = AsyncRabbitSender()


def bot_crashed(task: asyncio.Task):
    try:
        task.result()
    except Exception as e:
        bot_id = int(task.get_name())
        running_bots.pop(bot_id)
        bot: Bot = session.query(Bot).filter(Bot.bot_id == bot_id).one_or_none()
        bot.is_launched = False
        session.commit()



def run_bot(bot: Bot) -> None:
    bot_instance = AbstractBot(bot, sender)
    task = asyncio.create_task(bot_instance.run(), name=str(bot_instance.bot_id))
    task.add_done_callback(bot_crashed)
    running_bots[bot.bot_id] = task


@asynccontextmanager
async def lifespan(fastapp: FastAPI):
    bots = session.query(Bot).filter(Bot.is_launched == True).all()
    for bot in bots:
        run_bot(bot)
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
        run_bot(bot)
        bot.is_launched = True
    else:
        task = running_bots.pop(bot_id)
        task.cancel()
        await task
        bot.is_launched = False
    session.commit()
    return {"message": "Deployed" if bot.is_launched == True else "Stopped"}



