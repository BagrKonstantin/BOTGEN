import telebot
import json
from telebot.types import KeyboardButton, InlineKeyboardButton
from Stage import Stage

with open("config.json", "r") as f:
    config = json.load(f)


stages = []
for stage in config["stages"]:
    stages.append(stage["name"])