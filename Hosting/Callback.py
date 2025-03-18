from graph.encrypter import get_number
from telebot.types import CallbackQuery

class Callback:
    def __init__(self, chat_id: int, mes_id: int, calldata: str):
        self.chat_id = chat_id
        self.mes_id = mes_id
        stage, data = calldata[0], list(calldata[1:])
        self.current_stage = get_number(stage)
        self.data = data

    def get_option(self, stage: int) -> str:
        return self.data[stage]

    def is_true(self, stage: str, answer: str) -> bool:
        return self.data[get_number(stage)] == answer

    def is_back(self, stage: int) -> bool:
        return self.data[stage] == "~"

    def set_to_zero(self, stage: int):
        self.data[stage] = "0"
