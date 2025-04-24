from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

from utils.Callback import Callback


class AbstractStage:
    def __init__(self, stage: int, keyboard):
        self.stage = stage
        self.back_button = keyboard["back_button"]
        self.buttons = []
        for option, button in keyboard["buttons"].items():
            self.buttons.append((option, button["text"]))


    async def send(self, callback: Callback, bot: AsyncTeleBot):
        pass


    def make_keyboard(self, callback: Callback) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        for option, text in self.buttons:
            button_callback = callback.get_callback_string(self.stage, option)
            keyboard.add(InlineKeyboardButton(text=text, callback_data=button_callback))
        if self.back_button and self.stage != 0:
            button_callback = callback.get_callback_string(self.stage, '~')
            keyboard.add(InlineKeyboardButton(text="◀️Назад", callback_data=button_callback))
        return keyboard

    @staticmethod
    def get_stage(stage: int, data):
        if data["type"] == "text":
            return TextStage(stage, data)
        if data["type"] == "image":
            return ImageStage(stage, data)
        if data["type"] == "product":
            return ProductStage(stage, data)


class TextStage(AbstractStage):
    def __init__(self, stage, data):
        super().__init__(stage, data["keyboard"])
        self.text = data["text"]

    async def send(self, callback: Callback, bot: AsyncTeleBot):
        await bot.send_message(
            chat_id=callback.chat_id,
            text=self.text,
            reply_markup=self.make_keyboard(callback),
        )
        await bot.delete_message(callback.chat_id, callback.mes_id)

class ImageStage(AbstractStage):
    def __init__(self, stage, data):
        super().__init__(stage, data["keyboard"])
        self.text = data["text"]
        self.image = data["image"]

    async def send(self, callback: Callback, bot: AsyncTeleBot):
        await bot.send_photo(
            chat_id=callback.chat_id,
            photo=self.image,
            caption=self.text,
            reply_markup=self.make_keyboard(callback),
        )
        await bot.delete_message(callback.chat_id, callback.mes_id)


class ProductStage(AbstractStage):
    def __init__(self, stage, data):
        super().__init__(stage, data["keyboard"])
        self.title = data["product"]["title"]
        self.description = data["product"]["description"]
        self.price = data["product"]["price"]
        if "image_url" in data["product"]:
            self.image_url = data["product"]["image_url"]

    async def send(self, callback: Callback, bot: AsyncTeleBot):
        prices = [
            LabeledPrice(label="XTR", amount=self.price)
        ]


        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f"Оплатить {self.price} XTR", pay=True))
        if self.back_button:
            button_callback = callback.get_callback_string(self.stage, '~')
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data=button_callback))
        await bot.send_invoice(
            chat_id=callback.chat_id,
            title=self.title,
            description=self.description,
            prices=prices,
            provider_token="",
            invoice_payload=self.title,
            currency="XTR",
            reply_markup=keyboard,
            # photo_url=self.image_url TODO

        )
        await bot.delete_message(callback.chat_id, callback.mes_id)