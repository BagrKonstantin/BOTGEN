from pydantic import BaseModel

class Button(BaseModel):
    id: str
    text: str

class Keyboard(BaseModel):
    buttons: list[Button]

class Stage(BaseModel):
    id: str
    name: str
    text: str
    position: dict[str, int]
    keyboard: Keyboard = None
    imageId: str = None

class BotData(BaseModel):
    stages: list[Stage]

class Notifications(BaseModel):
    on_new_user: bool
    on_product_sold: bool
    on_out_of_stock: bool

class BotSettings(BaseModel):
    name: str
    token: str
    greeting_message: str
    notifications: Notifications
