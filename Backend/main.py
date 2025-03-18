from fastapi import FastAPI
from bot_service import send_auth_request
from pydantic import BaseModel
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post("/login/{username}")
async def request_login(username: str):
    # TODO database
    send_auth_request(username)
    return {"message": f"Go to telegram and accept"}

class TelegramRequest(BaseModel):
    token: str
    user_id: int
@app.post("/telebot-auth-accepted")
def auth_user(data: TelegramRequest):
    print(data)
    return "All fine"

