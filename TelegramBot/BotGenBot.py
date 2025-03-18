from telebot import TeleBot
import os
import requests

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

TELEGRAM_TOKEN = os.environ['TOKEN']
bot = TeleBot(token=TELEGRAM_TOKEN)

data = {}

@bot.message_handler(commands=['start'])
def message_handler(message: Message):
    # TODO SAVE TO DB
    data[message.from_user.username] = message.from_user.id
    print(data)


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