from utils.encrypter import get_number, get_char


class Callback:
    def __init__(self, chat_id: int, mes_id: int, calldata: str):
        self.chat_id = chat_id
        self.mes_id = mes_id
        dialog, stage, data = calldata[0], calldata[1], list(calldata[2:])
        self.current_dialog: int = get_number(dialog)
        self.current_stage: int = get_number(stage)
        self.data = data

    def get_option(self, stage: int) -> str:
        return self.data[stage]

    def is_true(self, stage: str, answer: str) -> bool:
        return self.data[get_number(stage)] == answer

    def is_back(self, stage: int) -> bool:
        return self.data[stage] == "~"

    def set_to_zero(self, stage: int):
        self.data[stage] = "*"

    def get_callback_string(self, stage: int, option: str) -> str:
        stage_char = get_char(stage)
        dialog_char = get_char(self.current_dialog)
        char = self.data[stage]
        self.data[stage] = option
        button_callback = dialog_char + stage_char + "".join(self.data)
        self.data[stage] = char
        print(button_callback)
        return button_callback


    @staticmethod
    def get_start(dialog, chat_id, mes_id):
        return Callback(chat_id, mes_id, dialog + '0' + '*' * 62)