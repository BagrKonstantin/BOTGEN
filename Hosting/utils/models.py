from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Bot(Base):
    __tablename__ = "bots"

    bot_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String())
    token = Column(String())
    data_json = Column(JSON)
    is_launched = Column(Boolean())
    greeting_message = Column(String())

    notify_on_sold = Column(Boolean())
    notify_on_out_of_stock = Column(Boolean())

    user = relationship("User", back_populates="bots")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key=True)
    tel_id = Column(Integer())

    bots = relationship("Bot", back_populates="user")

class ProductType(Base):
    __tablename__ = "product_types"

    product_type_id = Column(Integer(), primary_key=True)
    bot_id = Column(Integer())
    name = Column(String())

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer(), primary_key=True)
    product_type_id = Column(Integer())
    file_id = Column(String())
    is_sold = Column(Boolean(), default=False)
    bot_user_id = Column(Integer())

    def __str__(self):
        return f"{self.product_id, self.file_id, self.is_sold}"


# bot = session.query(Bot).filter(Bot.bot_id == 22).one()
# print(bot.user.tel_id)