import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends

from config import session
from routes import auth, bots, products
from services.auth_service import verify_token
from services.listener_service import start_consumer

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

# app.add_middleware(
#     CORSMiddleware,
#     # allow_origin_regex="http://localhost:5173/*",
#     allow_origin_regex="http://*",
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth.router)
app.include_router(bots.router)
app.include_router(products.router)




# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)
#     asyncio.run(start_consumer())
#     print("gag")

