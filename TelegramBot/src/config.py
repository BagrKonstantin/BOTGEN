import os
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

env = os.environ

TELEGRAM_TOKEN = env['TOKEN']

POSTGRESQL_USERNAME = env['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = env['POSTGRESQL_PASSWORD']
POSTGRESQL_DATABASE = env['POSTGRESQL_DATABASE']
POSTGRESQL_HOST = env['POSTGRESQL_HOST']
POSTGRESQL_PORT = int(env['POSTGRESQL_PORT'])

DOMAIN = env['DOMAIN']
SUBSCRIPTION_PRICE = int(env['SUBSCRIPTION_PRICE'])


RABBITMQ_URL = f"amqp://{env['RABBITMQ_USERNAME']}:{env['RABBITMQ_PASSWORD']}@{env['RABBITMQ_HOST']}/"
QUEUE_NAME = env["RABBITMQ_QUEUE"]

url = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USERNAME,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT,
    database=POSTGRESQL_DATABASE,
    password=POSTGRESQL_PASSWORD
)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
