import os
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession

env = os.environ

TELEGRAM_TOKEN = env['TOKEN']
POSTGRESQL_USERNAME = env['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = env['POSTGRESQL_PASSWORD']
POSTGRESQL_HOST = env['POSTGRESQL_HOST']


RABBITMQ_HOST = env['RABBITMQ_HOST']
RABBITMQ_URL = f"amqp://guest:guest@{RABBITMQ_HOST}/"

HOSTING_HOST = env['HOSTING_HOST']

HOSTING_URL = f"http://{HOSTING_HOST}:8080"



QUEUE_NAME = "my_queue"

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = f"postgresql+asyncpg://{POSTGRESQL_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:5432/postgres"

# DATABASE_URL = URL.create(
#     drivername="postgresql",
#     username=POSTGRESQL_USERNAME,
#     host=POSTGRESQL_HOST,
#     database="postgres",
#     password=POSTGRESQL_PASSWORD
# )

engine = create_async_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
session: AsyncSession = AsyncSession(engine)
