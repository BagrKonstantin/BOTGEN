import logging
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from telebot import TeleBot
import os
import requests
from sqlalchemy.engine import URL
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, LabeledPrice
from sqlalchemy.orm import sessionmaker
from models import User, Subscription

env = os.environ
TELEGRAM_TOKEN = env['TOKEN']
POSTGRESQL_USERNAME = env['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = env['POSTGRESQL_PASSWORD']
POSTGRESQL_HOST = env['POSTGRESQL_HOST']

url = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USERNAME,
    host=POSTGRESQL_HOST,
    database="postgres",
    password=POSTGRESQL_PASSWORD
)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()



bot = TeleBot(token=TELEGRAM_TOKEN)

data = {}

@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    # TODO rabbitmq
    tel_id = message.from_user.id
    username = message.from_user.username.lower()
    user = session.query(User).filter(User.tel_id == tel_id).one_or_none()
    if user:
        user.username = username
    else:
        user = User(tel_id=tel_id, username=username)
        session.add(user)
    session.commit()

@bot.message_handler(commands=['pay'])
def payment_handler(message: Message):
    prices = [
        LabeledPrice(label="XTR", amount=1)
    ]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f"Оплатить {1} XTR", pay=True))
    bot.send_invoice(
        chat_id=message.from_user.id,
        title="Хостинг",
        description="Оплата хостинга на месяц",
        prices=prices,
        provider_token="",
        invoice_payload=f"hosting:{message.from_user.id}",
        currency="XTR",

        # need_name=True,
        # need_phone_number=True,
        # need_email=True,
        # need_shipping_address=True
    )

@bot.pre_checkout_query_handler(func=lambda query: query.invoice_payload.startswith("hosting"))
def hosting_checkout_handler(query):
    print(query)
    tel_id = int(query.from_user.id)
    user = session.query(User).filter(User.tel_id == tel_id).one_or_none()
    subscription = session.query(Subscription).filter(Subscription.user_id == user.user_id and Subscription.expiration_date > datetime.today()).one_or_none()
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
    bot.answer_pre_checkout_query(query.id, True)
    logging.info(f"User {user.user_id}, with tel_id: {tel_id} purchased subscription for month")
    bot.send_message(tel_id, text=f"Хостинг оплачен до {subscription.expiration_date.strftime("%d.%m.%Y")}")



@bot.callback_query_handler(func=lambda call: "auth_" in call.data)
def auth_query(call):
    if call.data.startswith("auth_accept"):
        token = call.data.split(":")[1]
        print(call.message.chat.id)
        response = requests.post("http://127.0.0.1:8000/telebot-auth-accepted",
                                 json={
                                     "token": token,
                                     "user_id": call.message.chat.id
                                 })
        print(response.text)
        if response.status_code == 200:
            bot.answer_callback_query(call.id, "Вы успешно авторизованы")
        else:
            bot.answer_callback_query(call.id, "Что-то пошло не так, попробуйте позже")


    elif call.data.startswith("auth_decline"):
        pass
    else:
        bot.answer_callback_query(call.id, "Что-то пошло не так, попробуйте позже")


bot.infinity_polling()
