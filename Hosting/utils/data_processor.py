import json

from utils.encrypter import line


def process_raw(bot: str):

    dialog_characters = str(line)


    data = json.loads(bot)
    dialogs = data["dialogs"]
    for dialog_key, dialog_value in dialogs.items():
        dialog_value["char"] = dialog_characters[0]
        dialog_characters = dialog_characters[1:]

        stage_mapper = dict()
        stages: dict = dialog_value["stages"]
        options_mapper = dict()
        stages_characters = str(line)
        for stage_key, stage_value in stages.items():
            stage_mapper[stage_key] = stages_characters[0]
            stages_characters = stages_characters[1:]

        for stage_key, stage_value in stages.items():
            options = stage_value["keyboard"]["buttons"]
            options_character = str(line)
            option_mapper = dict()
            options_mapper[stage_key] = option_mapper
            for option_key, option_value in options.items():
                option_mapper[option_key] = options_character[0]
                options_character = options_character[1:]

                if option_value["to"] in stage_mapper.keys():
                    option_value["to"] = stage_mapper[option_value["to"]]



            for option_key, option_value in option_mapper.items():

                options[option_mapper[option_key]] = options.pop(option_key)



        for stage_key, stage_value in stage_mapper.items():
            options_mapper[stage_mapper[stage_key]] = options_mapper.pop(stage_key)
            stages[stage_mapper[stage_key]] = stages.pop(stage_key)

        stages = dialog_value["stages"]
        for stage_key, stage_value in stages.items():
            options = stage_value["keyboard"]["buttons"]
            for option_key, option_value in options.items():
                if "if" in option_value:
                    option_value["if"]["stage"] = stage_mapper[option_value["if"]["stage"]]
                    option_value["if"]["to"] = stage_mapper[option_value["if"]["to"]]

                    option_value["if"]["equals"] = options_mapper[stage_key][option_value["if"]["equals"]]

    return data