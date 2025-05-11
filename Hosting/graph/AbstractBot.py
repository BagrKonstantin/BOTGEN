import json
import logging
from itertools import product

import telebot
from sqlalchemy import select
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, CallbackQuery, InlineQueryResultArticle, InputTextMessageContent

from graph.Graph import Graph
from graph.Stages import ProductStage
from service.sender_service import AsyncRabbitSender
from utils.Callback import Callback
from utils.config import session
from utils.data_processor import process_raw
from utils.encrypter import get_number
from utils.models import Bot
from utils.models import ProductType, Product


class AbstractBot:
    def __init__(self, bot: Bot, sender: AsyncRabbitSender):
        self.owner = bot.user.tel_id
        self.notify_on_sold = bot.notify_on_sold
        self.notify_on_out_of_stock = bot.notify_on_out_of_stock

        self.sender = sender

        self.graphs = list()
        self.dialogs = dict()
        self.dialog_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        self.products: list[ProductStage] = list()
        self.process_data(bot.data_json)

        self.greeting_message:str = bot.greeting_message
        self.bot: AsyncTeleBot = AsyncTeleBot(bot.token)
        self.bot_id: int = bot.bot_id
        self.username = ""


    def process_data(self, json_data):
        try:
            data = process_raw(json_data)
            for dialog_key, dialog_value in data["dialogs"].items():
                graph = Graph(dialog_value["stages"])
                self.products += graph.products
                self.graphs.append(graph)
                self.dialogs[dialog_key] = dialog_value["char"]
            for dialog in self.dialogs.keys():
                self.dialog_keyboard.add(dialog)
        except Exception:
            raise RuntimeError("Your bot has cyclic dependencies and/or unfinished routes")

    async def callback_query(self, call: CallbackQuery):
        callback = Callback(call.message.chat.id, call.message.id, call.data)
        cur_graph = self.graphs[callback.current_dialog]
        node = cur_graph.get_stage(callback)
        await node.stager.send(callback, self.bot)
        await self.bot.answer_callback_query(call.id)

    async def send_greeting_message(self, message: Message):
        chat_id, mes_id = message.from_user.id, message.message_id
        await self.sender.send(json.dumps({
            "type": "new_user",
            "bot_id": self.bot_id,
            "tel_id": message.from_user.id,
        }))

        await self.bot.send_message(chat_id, self.greeting_message, reply_markup=self.dialog_keyboard)


    async def choose_dialog(self, message: Message):
        if message.text in self.dialogs.keys():
            dialog_char = self.dialogs[message.text]
            dialog_number = get_number(dialog_char)
            node = self.graphs[dialog_number].start
            callback = Callback.get_start(dialog_char, message.from_user.id, message.message_id)
            await node.stager.send(callback, self.bot)
        else:
            await self.send_greeting_message(message)


    async def checkout_handler(self, query):
        tel_id = int(query.from_user.id)
        product_type = session.scalar(select(ProductType).where(ProductType.name == query.invoice_payload, ProductType.bot_id == self.bot_id))
        product = session.scalars(select(Product).where(Product.product_type_id == product_type.product_type_id, Product.is_sold == False)).first()
        # product: Product = session.query(Product).filter(Product.product_type_id == product_type.product_type_id).filter(Product.is_sold == False).one_or_none()
        if product is None:
            await self.bot.answer_pre_checkout_query(query.id, False, error_message="Sold out")
            await self.bot.send_message(self.owner, f"User tried to purchase product {query.invoice_payload}, but it's out of stock")
            return
        product.is_sold = True
        product.bot_user_id = tel_id
        session.commit()
        session.refresh(product)
        await self.bot.send_document(tel_id, product.file_id, caption=product_type.name)
        await self.bot.answer_pre_checkout_query(query.id, True)
        if self.notify_on_sold:
            await self.bot.send_message(self.owner, f"Product {query.invoice_payload} was sold")
        if self.notify_on_out_of_stock:
            product = session.scalars(select(Product).where(Product.product_type_id == product_type.product_type_id, Product.is_sold == False)).first()
            if product is None:
                await self.bot.send_message(self.owner, f"Product {query.invoice_payload} is out of stock")

    def make_buy_keyboard(self, product_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="View product", callback_data=f"buy:{product_id}"))
        return keyboard

    async def inline_query_handler(self, query: InlineQuery):
        logging.info(f"Handling inline query: {query}")
        results = []
        for product_id, product in enumerate(self.products):
            if query.query.lower() in product.title.lower() or query.query.lower() in product.description.lower():
                results.append(InlineQueryResultArticle(
                    id=product_id,
                    title=product.title,
                    description=product.description,
                    reply_markup=self.make_buy_keyboard(product_id),
                    thumbnail_url=product.image_url,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{product.title}\n\n{product.description}",
                    )
                ))
        await self.bot.answer_inline_query(query.id, results[:50])

    async def buy_callback_query(self, call: CallbackQuery):
        product_id = int(call.data.split(":")[1])
        try:
            await self.products[product_id].send_without_callback(self.bot, call.from_user.id)
            await self.bot.answer_callback_query(call.id, text=f"You can purchase product in @{self.username}", show_alert=True)
        except telebot.async_telebot.asyncio_helper.ApiException:
            await self.bot.answer_callback_query(call.id, text=f"You need to start @{self.username} first", show_alert=True)


    async def try_token(self):
        bot = await self.bot.get_me()
        self.username = bot.username

    async def run(self):
        self.bot.register_callback_query_handler(callback=self.buy_callback_query, func=lambda x: x.data.startswith("buy"))
        self.bot.register_callback_query_handler(callback=self.callback_query, func=lambda x: x)
        self.bot.register_message_handler(callback=self.send_greeting_message, commands=['start'])
        self.bot.register_message_handler(callback=self.choose_dialog, content_types=['text'])
        self.bot.register_pre_checkout_query_handler(callback=self.checkout_handler, func=lambda x: x)
        self.bot.register_inline_handler(callback=self.inline_query_handler, func=lambda x: x)
        await self.bot.infinity_polling()

