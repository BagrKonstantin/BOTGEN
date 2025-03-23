from graph.Graph import Graph
import telebot
from Callback import Callback
from graph.Stages import AbstractStage


class AbstractBot:
    def __init__(self, token, config):
        self.graph = Graph(config["stages"])
        self.bot: telebot.TeleBot = telebot.TeleBot(token)

    def callback_query(self, call):
        callback = Callback(call.message.chat.id, call.message.id, call.data)
        node = self.graph.get_stage(callback)
        print(callback.data)
        node.stager.send(callback, self.bot)
        self.bot.answer_callback_query(call.id, "Ответ")

    def send_message(self, message: telebot.types.Message):
        print(message)
        chat_id, mes_id = message.from_user.id, message.message_id
        node = self.graph.start
        callback = Callback(chat_id, mes_id, "0000000000000000000000000000000000000000000000000000000000000000")
        node.stager.send(callback, self.bot)

    def run(self):
        self.bot.register_callback_query_handler(callback=self.callback_query, func=lambda x: x)
        self.bot.register_message_handler(callback=self.send_message, content_types=["text"])
        self.bot.infinity_polling()
