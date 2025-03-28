from telebot import TeleBot
import os
import random
import string
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import User


env = os.environ
TELEGRAM_TOKEN = env['TOKEN']

bot = TeleBot(token=TELEGRAM_TOKEN)


def make_keyboard(token: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="✅ Авторизоваться", callback_data=f"auth_accept:{token}"))
    keyboard.add(InlineKeyboardButton(text="❌ Это не я", callback_data="auth_decline"))

    return keyboard


def send_auth_request(users: list[User]):
    for user in users:
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        keyboard = make_keyboard(token)

        bot.send_message(user.tel_id, "Новый запрос на авторизацию.\nЕсли это вы - нажмите 'Авторизоваться'.",
                         reply_markup=keyboard)
