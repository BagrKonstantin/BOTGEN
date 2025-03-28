from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

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