from pydantic import BaseModel

class TelegramRequest(BaseModel):
    token: str
    user_id: int
