from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
from graph.Graph import Graph
from AbstractBot import AbstractBot

app = FastAPI()

bots: dict[str, (AbstractBot, Thread)] = {}


@app.post("/launch/{bot_id}")
async def launch_bot(bot_id):
    # TODO database
    import json
    token = "7485571734:AAEJk02Oh1k10MUhwtRaQ3VjPHU9eS5bDvA"
    with open("etna.json", "r", encoding="utf-8") as file:
        data_raw = json.load(file)

    bot = AbstractBot(token, data_raw)
    thread = Thread(target=bot.run)

    bots[bot_id] = (bot, thread)
    thread.start()

    return {"message": f"Deployed"}


@app.post("/stop/{bot_id}")
async def stop_bot(bot_id):
    # TODO database

    bots[bot_id][0].stop()
    bots[bot_id][1].join()

    return {"message": f"Stopped"}
