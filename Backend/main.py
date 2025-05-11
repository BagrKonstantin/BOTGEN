import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, bots, products
from service.auth_service import verify_token
from service.listener_service import start_consumer
from utils.config import session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)



@asynccontextmanager
async def lifespan(fastapp: FastAPI):
    task = asyncio.create_task(start_consumer())
    yield
    await session.close()
    task.cancel()


app = FastAPI(
    dependencies=[Depends(verify_token)],
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://botgen-constructor.ru/api/*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(bots.router)
app.include_router(products.router)
