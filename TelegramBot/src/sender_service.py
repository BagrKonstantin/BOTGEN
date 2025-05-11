from src.config import RABBITMQ_URL
from aio_pika import connect_robust, Message

class AsyncRabbitSender:
    def __init__(self, amqp_url=RABBITMQ_URL, queue_name="my_queue"):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

        await self.channel.declare_queue(self.queue_name, durable=True)

    async def send(self, message: str):
        if self.connection is None:
            await self.connect()
        if self.channel.closed():
            await self.connect()

        await self.channel.default_exchange.publish(
            Message(body=message.encode(), delivery_mode=2),
            routing_key=self.queue_name
        )

    async def close(self):
        await self.connection.close()
