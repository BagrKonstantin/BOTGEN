from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
from graph.Graph import Graph
from AbstractBot import AbstractBot

app = FastAPI()

bots = {}

@app.post("/launch/{bot_id}")
async def launch_bot(bot_id):
    # TODO database
    import json
    token = "7485571734:AAGAy6vt0eRMWxEbYT4zPXeqLnGX09GP8gA"
    with open("etna.json", "r", encoding="utf-8") as file:
        data_raw = json.load(file)

    bot = AbstractBot(token, data_raw)
    thread = Thread(target=bot.run)

    bots[bot_id] = thread
    bots[bot_id].start()

    print(1)

    return {"message": f"Deployed"}