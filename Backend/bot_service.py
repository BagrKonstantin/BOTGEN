from telebot import TeleBot
import os
import random
import string

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = os.environ['TOKEN']
bot = TeleBot(token=TELEGRAM_TOKEN)

data = {"bagrkonstantin": 171303452}


def make_keyboard(token: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="✅ Авторизоваться", callback_data=f"auth_accept:{token}"))
    keyboard.add(InlineKeyboardButton(text="❌ Это не я", callback_data="auth_decline"))

    return keyboard


def send_auth_request(username: str):
    user_id = data[username]

    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
    keyboard = make_keyboard(token)

    bot.send_message(user_id, "Новый запрос на авторизацию.\nЕсли это вы - нажмите 'Авторизоваться'.",
                     reply_markup=keyboard)

    return token