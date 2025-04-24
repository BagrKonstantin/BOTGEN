from telebot import TeleBot
import random
import string
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, PhotoSize, LabeledPrice, Message, File
from schemas.models import User
from config import TELEGRAM_TOKEN

bot = TeleBot(token=TELEGRAM_TOKEN)


def make_keyboard(token: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🔓 Authorize", callback_data=f"auth_accept:{token}"))
    #keyboard.add(InlineKeyboardButton(text="❌ Это не я", callback_data=f"auth_decline:{token}"))

    return keyboard


def send_auth_request(user: User):
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
    bot.send_message(user.tel_id, """Hey! 👋
To connect your Telegram account with the BotGen platform, please authorize your access.

Just click the button below to confirm and get started building your bot! 🤖"
""",
    reply_markup=make_keyboard(token))
    return token


def send_image(user_id, bot_token, image) -> str:
    temporal_bot = TeleBot(token=bot_token)
    message: Message = temporal_bot.send_photo(user_id, photo=image)
    temporal_bot.delete_message(message.chat.id, message.message_id)
    photos: list[PhotoSize] = message.photo
    image_id = sorted(photos, key=lambda file: file.file_size)[-1].file_id
    return image_id

def get_image(bot_token, image_id) -> bytes:
    temporal_bot = TeleBot(token=bot_token)
    file: File = temporal_bot.get_file(image_id)
    return temporal_bot.download_file(file.file_path)

def send_file(user_id, bot_token, file, filename) -> str:
    temporal_bot = TeleBot(token=bot_token)
    message: Message = temporal_bot.send_document(user_id, file, visible_file_name=filename)
    temporal_bot.delete_message(message.chat.id, message.message_id)
    return message.document.file_id

def send_new_user_message(bot_token, tel_id):
    temporal_bot = TeleBot(token=bot_token)
    temporal_bot.send_message(tel_id, "You have new user!")

def send_payment(tel_id):
    prices = [
        LabeledPrice(label="XTR", amount=1)
    ]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f"Оплатить {1} XTR", pay=True))
    bot.send_invoice(
        chat_id=tel_id,
        title="Хостинг",
        description="Оплата хостинга на месяц",
        prices=prices,
        provider_token="",
        invoice_payload=f"hosting:{tel_id}",
        currency="XTR",
    )


