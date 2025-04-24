import os
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

env = os.environ

POSTGRESQL_USERNAME = env['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = env['POSTGRESQL_PASSWORD']
POSTGRESQL_HOST = env['POSTGRESQL_HOST']

RABBITMQ_HOST = env['RABBITMQ_HOST']
RABBITMQ_URL = f"amqp://guest:guest@{RABBITMQ_HOST}/"

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=POSTGRESQL_USERNAME,
    host=POSTGRESQL_HOST,
    database="postgres",
    password=POSTGRESQL_PASSWORD
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
