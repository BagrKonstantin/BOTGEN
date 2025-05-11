import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

env = os.environ

POSTGRESQL_USERNAME = env['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = env['POSTGRESQL_PASSWORD']
POSTGRESQL_DATABASE = env['POSTGRESQL_DATABASE']
POSTGRESQL_HOST = env['POSTGRESQL_HOST']

RABBITMQ_URL = f"amqp://{env['RABBITMQ_USERNAME']}:{env['RABBITMQ_PASSWORD']}@{env['RABBITMQ_HOST']}/"
QUEUE_NAME = env["RABBITMQ_QUEUE"]

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USERNAME,
    host=POSTGRESQL_HOST,
    database=POSTGRESQL_DATABASE,
    password=POSTGRESQL_PASSWORD
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
