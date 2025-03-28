from fastapi import FastAPI
from bot_service import send_auth_request
from pydantic import BaseModel
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from models import User

env = os.environ
TELEGRAM_TOKEN = env['TOKEN']
POSTGRESQL_USERNAME = env['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = env['POSTGRESQL_PASSWORD']
POSTGRESQL_HOST = env['POSTGRESQL_HOST']

url = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USERNAME,
    host=POSTGRESQL_HOST,
    database="postgres",
    password=POSTGRESQL_PASSWORD
)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()


@app.post("/login/{username}")
async def request_login(username: str):
    username = username.lower()
    users = session.query(User).filter(User.username == username).all()
    send_auth_request(users)
    return {"message": f"Go to telegram and accept"}

class TelegramRequest(BaseModel):
    token: str
    user_id: int

@app.post("/telebot-auth-accepted")
def auth_user(data: TelegramRequest):
    print(data)
    return "All fine"

@app.post("/telebot-auth-rejected")
def auth_user(data: TelegramRequest):
    print(data)

`


