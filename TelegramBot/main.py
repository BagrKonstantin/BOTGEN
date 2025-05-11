import asyncio
import json
import logging
from datetime import datetime, timedelta

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, LabeledPrice, CallbackQuery

from src.models import User, Subscription
from src.sender_service import AsyncRabbitSender

from src.config import TELEGRAM_TOKEN, session, DOMAIN, SUBSCRIPTION_PRICE

bot = AsyncTeleBot(token=TELEGRAM_TOKEN)

data = {}

def make_start_keyboard(username: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Access your account", url=f"{DOMAIN}/?username={username}"))
    keyboard.add(InlineKeyboardButton(text="My subscription", callback_data="subscription"))
    return keyboard

def make_sub_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Refresh", callback_data="refresh"))
    keyboard.add(InlineKeyboardButton(text="Purchase", callback_data="purchase"))
    return keyboard


@bot.message_handler(commands=['start'])
async def start_handler(message: Message):
    tel_id = message.from_user.id
    username = message.from_user.username.lower()
    user = session.query(User).filter(User.tel_id == tel_id).one_or_none()
    if user:
        user.username = username
    else:
        user = User(tel_id=tel_id, username=username)
        session.add(user)
    session.commit()
    await bot.send_message(
        tel_id,
        text=f"""Hello\! 👋 Welcome to *BotGen* – your easy tool for creating Telegram bots without any programming knowledge\. 
To get started, simply visit our [web platform](https://botgen-constructor.ru) where you can design your bot and deploy it in no time\! 🌐

To access your account, use username \@{username} or click button below\.
Let’s build your bot together\! 💡
""", reply_markup=make_start_keyboard(username), parse_mode="MarkdownV2"
    )

def get_subscription(tel_id):
    user = session.query(User).filter(User.tel_id == tel_id).one_or_none()
    subscription = session.query(Subscription).filter(Subscription.user_id == user.user_id, Subscription.expiration_date > datetime.today()).one_or_none()
    return subscription

def make_subscription_message(subscription):
    return f"""Here's your current subscription info:

Status: {"Active✅" if subscription else "Inactive❌"}
{f"Ends on: {subscription.expiration_date.strftime('%d.%m.%Y')}" if subscription else ""}
"""

async def send_invoice(tel_id):
    prices = [
        LabeledPrice(label="XTR", amount=SUBSCRIPTION_PRICE)
    ]
    await bot.send_invoice(
        chat_id=tel_id,
        title="Bot Hosting Subscription",
        description="""Host your Telegram bot 24/7 with BotGen!
This subscription includes:

🚀 Instant bot deployment

🔄 Auto-restart on failure

🛠 Easy updates through the web constructor

💬 Message delivery via high-speed queues

🧠 Zero code needed – manage everything visually

Stay focused on building, we’ll handle the hosting.""",
        prices=prices,
        provider_token="",
        invoice_payload=f"hosting:{tel_id}",
        currency="XTR",
    )


@bot.callback_query_handler(func=lambda call: call.data == "subscription")
async def auth_query(call: CallbackQuery):
    subscription = get_subscription(call.from_user.id)
    await bot.send_message(call.from_user.id,make_subscription_message(subscription), reply_markup=make_sub_keyboard())
    await bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "refresh")
async def refresh_query(call: CallbackQuery):
    subscription = get_subscription(call.from_user.id)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=make_subscription_message(subscription), reply_markup=make_sub_keyboard())
    except ApiTelegramException:
        pass
    await bot.answer_callback_query(call.id, "Refreshed")


@bot.callback_query_handler(func=lambda call: call.data == "purchase")
async def purchase_query(call: CallbackQuery):
    await send_invoice(call.from_user.id)
    await bot.answer_callback_query(call.id)

@bot.message_handler(commands=['pay'])
async def payment_handler(message: Message):
    await send_invoice(message.from_user.id)


@bot.pre_checkout_query_handler(func=lambda query: query.invoice_payload.startswith("hosting"))
async def hosting_checkout_handler(query):
    tel_id = int(query.from_user.id)
    user = session.query(User).filter(User.tel_id == tel_id).one_or_none()
    subscription = session.query(Subscription).filter(Subscription.user_id == user.user_id, Subscription.expiration_date > datetime.today()).one_or_none()
    if subscription:
        subscription.expiration_date += timedelta(days=30)
    else:
        subscription = Subscription(
            user_id=user.user_id,
            start_date=datetime.today(),
            expiration_date=datetime.today() + timedelta(days=30),
        )
        session.add(subscription)

    session.commit()
    await bot.answer_pre_checkout_query(query.id, True)
    logging.info(f"User {user.user_id}, with tel_id: {tel_id} purchased subscription for month")
    await bot.send_message(query.from_user.id,make_subscription_message(subscription), reply_markup=make_sub_keyboard())



@bot.callback_query_handler(func=lambda call: call.data.startswith("auth_"))
async def auth_query(call: CallbackQuery):
    is_approved = call.data.startswith("auth_accept")
    token = call.data.split(":")[1]
    await sender.send(json.dumps({
        "type": "auth",
        "is_approved": is_approved,
        "user_id": call.from_user.id,
        "token": token
    }))
    print("sent")
    await bot.answer_callback_query(call.id, ("You successfully authorized" if is_approved else "Authorization canceled"))
    await bot.delete_message(call.message.chat.id, call.message.message_id)


sender = AsyncRabbitSender()

async def main():
    await sender.connect()
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())
