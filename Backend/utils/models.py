from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key=True)
    tel_id = Column(Integer())
    username = Column(String())


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    start_date = Column(DateTime())
    expiration_date = Column(DateTime())


class Bot(Base):
    __tablename__ = "bots"

    bot_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    name = Column(String(), default='bot')
    token = Column(String())
    data_json = Column(JSON, default="{\"dialogs\": {\"Start\": {\"stages\": {}}}}")
    is_launched = Column(Boolean(), default=False)
    greeting_message = Column(String(), default="Hello, I'm bot made with BotGen")

    notify_on_new_user = Column(Boolean(), default=False)
    notify_on_sold = Column(Boolean(), default=False)
    notify_on_out_of_stock = Column(Boolean(), default=False)

class BotUser(Base):
    __tablename__ = "bot_users"

    bot_user_id = Column(Integer(), primary_key=True)
    tel_id = Column(Integer())
    bot_id = Column(Integer())


class ProductType(Base):
    __tablename__ = "product_types"

    product_type_id = Column(Integer(), primary_key=True)
    bot_id = Column(Integer())
    name = Column(String())
    price = Column(Integer())


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer(), primary_key=True)
    product_type_id = Column(Integer())
    file_id = Column(String())
    is_sold = Column(Boolean(), default=False)
    bot_user_id = Column(Integer())
