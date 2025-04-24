import asyncio
import json

from aio_pika import connect_robust
from sqlalchemy import select

from routes.auth import users_dic
from config import QUEUE_NAME, RABBITMQ_URL
from schemas.models import BotUser, Bot, User
from config import session
from services.bot_service import send_new_user_message


async def process_message(message):
    async with message.process():
        message_json = json.loads(message.body.decode())
        print(message_json)
        if message_json["type"] == "auth":
            if message_json["is_approved"]:
                users_dic[message_json["token"]] = message_json["user_id"]
        if message_json["type"] == "new_user":
            bot_user = await session.scalar(select(BotUser).where(BotUser.bot_id == message_json["bot_id"] and BotUser.tel_id==message_json["tel_id"]))
            if bot_user is None:
                session.add(BotUser(bot_id=message_json["bot_id"], tel_id=message_json["tel_id"]))
                bot = await session.get(Bot, message_json["bot_id"])
                if bot.notify_on_new_user:
                    user = await session.get(User, bot.user_id)
                    send_new_user_message(bot.token, user.tel_id)
                await session.commit()
        await asyncio.sleep(1)

async def start_consumer():
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(process_message)

    await asyncio.Future()

