import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

from Callback import Callback
from graph.encrypter import get_char


class AbstractStage:
    def __init__(self, stage: int, keyboard):
        self.stage = stage
        self.back_button = keyboard["back_button"]
        self.buttons = []
        for option, button in keyboard["buttons"].items():
            self.buttons.append((option, button["text"]))


    def send(self, callback: Callback, bot: telebot.TeleBot):
        pass


    def make_keyboard(self, callback: Callback) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        stage = get_char(self.stage)
        for option, text in self.buttons:
            callback.data[self.stage] = option
            button_callback = stage + "".join(callback.data)
            print("----", button_callback)
            keyboard.add(InlineKeyboardButton(text=text, callback_data=button_callback))
        if stage != '0':
            callback.data[self.stage] = "~"
            button_callback = stage + "".join(callback.data)
            print("----", button_callback)
            keyboard.add(InlineKeyboardButton(text="◀️Назад", callback_data=button_callback))
        return keyboard

    @staticmethod
    def get_stage(stage: int, data):
        if data["type"] == "image":
            return ImageStage(stage, data)
        if data["type"] == "product":
            return ProductStage(stage, data)


class TextStage(AbstractStage):
    def __init__(self, stage, data):
        super().__init__(stage, data["keyboard"])

class ImageStage(AbstractStage):
    def __init__(self, stage, data):
        super().__init__(stage, data["keyboard"])
        self.text = data["text"]
        self.image = data["image"]

    def send(self, callback: Callback, bot: telebot.TeleBot):
        bot.send_photo(
            chat_id=callback.chat_id,
            photo=open(self.image, "rb"),
            caption=self.text,
            reply_markup=self.make_keyboard(callback),
        )
        bot.delete_message(callback.chat_id, callback.mes_id)


class ProductStage(AbstractStage):
    def __init__(self, stage, data):
        super().__init__(stage, data["keyboard"])
        self.title = data["product"]["title"]
        self.description = data["product"]["description"]
        self.price = data["product"]["price"]
        self.image_url = data["product"]["image_url"]

    def send(self, callback: Callback, bot: telebot.TeleBot):
        prices = [
            LabeledPrice(label="XTR", amount=self.price)
        ]
        callback.data[self.stage] = "~"
        stage = get_char(self.stage)
        button_callback = stage + "".join(callback.data)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f"Оплатить {self.price} XTR", pay=True))
        keyboard.add(InlineKeyboardButton(text="Назад", callback_data=button_callback))
        bot.send_invoice(
            chat_id=callback.chat_id,
            title=self.title,
            description=self.description,
            prices=prices,
            provider_token="",
            invoice_payload="channel_support",
            currency="XTR",
            reply_markup=keyboard,
            photo_url=self.image_url

            # need_name=True,
            # need_phone_number=True,
            # need_email=True,
            # need_shipping_address=True
        )
        bot.delete_message(callback.chat_id, callback.mes_id)