from fastapi import APIRouter, Header, UploadFile, File

from service.auth_service import is_bot_owner, get_tel_id_from_header
from service.bot_service import get_bot
from service.product_service import *
from service.telegram_service import send_file
from utils.config import session
from utils.models import Bot, Product

router = APIRouter(prefix="/api")


@router.get("/get-all-product-types/{bot_id}")
async def get_product_types_endpoint(bot_id: int, authorization: str = Header(None)):
    bot: Bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    product_types = await get_product_types(bot_id)
    return product_types


@router.get("/get-all-products/{product_type_id}")
async def get_products_endpoint(product_type_id: int, authorization: str = Header(None)):
    product_type = await get_product_type(product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)

    products = get_products(product_type_id)
    return products


@router.post("/upload-product/{product_type_id}")
async def upload_product(product_type_id: int, file: UploadFile = File(...), authorization: str = Header(None)):
    product_type = await get_product_type(product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)

    tel_id = get_tel_id_from_header(authorization)
    contents = await file.read()

    file_id = send_file(tel_id, bot.token, contents, file.filename)
    product = Product(product_type_id=product_type.product_type_id, file_id=file_id)
    session.add(product)
    await session.commit()

    return product


@router.delete("/delete-product/{product_id}")
async def delete_product_endpoint(product_id: int, authorization: str = Header(None)):
    product = await get_product(product_id)
    product_type = await get_product_type(product.product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)

    await delete_product(product)


@router.delete("/delete-product-type/{product_type_id}")
async def delete_product_type_endpoint(product_type_id: int, authorization: str = Header(None)):
    product_type = await get_product_type(product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)

    await delete_product_type(bot, product_type)
