import os
from enum import Enum

import telebot
from graph.Graph import Graph
from graph.Node import Node
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, KeyboardButton, \
    LabeledPrice, CallbackQuery

from graph.Stages import ImageStage, ProductStage
from graph.encrypter import get_char
from graph.Stages import *


TELEGRAM_TOKEN = os.environ['TOKEN']

bot = telebot.TeleBot(TELEGRAM_TOKEN)

AbstractStage.bot = bot


import json

with open("etna.json", "r", encoding="utf-8") as file:
    data_raw = json.load(file)

graph = Graph(data_raw["stages"])




def send_message(chat_id, mes_id):
    node = graph.start
    callback = Callback(chat_id, mes_id, "0000000000000000000000000000000000000000000000000000000000000000")
    node.stager.send(callback)

def how_can_help(message):
    bot.reply_to(message, "Как я могу помочь?", reply_markup=main_keyboard)
def edit_message(node: Node, callback):
    node.stager.send(callback)

class BasicTexts(Enum):
    CHOOSE_PROGRAM = "🥗Подобрать программу"


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton(text=BasicTexts.CHOOSE_PROGRAM.value))


def send_greeting(chat_id, message_id):
    bot.send_photo(
        chat_id,
        photo=open("content/promo/promo.png", "rb"),
        caption="Привет! Я ETNA-бот помощник по программе «ЗОЖ Питание+Спорт» от Wellness ETNA.\nЯ помогу вам с подбором программы и дам полезные советы для достижения ваших целей!",
        reply_markup=main_keyboard,
        reply_to_message_id=message_id
    )

@bot.message_handler(commands=['start'])
def message_handler(message: Message):
    a = InlineKeyboardMarkup()
    a.add(InlineKeyboardButton(text="✅ Авторизоваться", callback_data="a"))
    a.add(InlineKeyboardButton(text="❌ Это не я", callback_data="b"))
    # bot.send_message(message.chat.id, "Новый запрос на авторизацию.\nЕсли это вы - нажмите 'Авторизоваться'.", reply_markup=a)
    prices = [
    LabeledPrice(label="XTR", amount=150)
    ]
    bot.send_invoice(message.chat.id, title="Хостнг", description="Плата за хостинг бота на 30 дней",
                     prices=prices,
    provider_token="",
    invoice_payload="channel_support",
    currency="XTR",
)
    # send_greeting(message.chat.id, message.message_id)

@bot.message_handler(content_types=["text"])
def message_reply(message):
    if message.text == BasicTexts.CHOOSE_PROGRAM.value:
        send_message(message.chat.id, message.message_id)
    else:
        how_can_help(message)



@bot.message_handler(content_types=['photo'])
def photo_handler(message: Message):
    print(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    callback = Callback(call.message.chat.id, call.message.id, call.data)
    node = graph.get_stage(callback)
    print(callback.data)
    edit_message(node, callback)
    bot.answer_callback_query(call.id, "Ответ")


bot.infinity_polling()