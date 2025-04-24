import json
from typing import Union

from fastapi import APIRouter, Header, UploadFile, File, HTTPException
from sqlalchemy import select, Sequence

from config import session
from schemas.models import Bot, ProductType, Product
from services.auth_service import  is_bot_owner, get_tel_id_from_header
from services.bot_service import send_file

router = APIRouter()

async def get_product(product_id: int) -> Product:
    product: Union[Product, None] = await session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def get_product_type(product_type_id: int) -> ProductType:
    product_type: Union[ProductType, None] = await session.get(ProductType, product_type_id)
    if product_type is None:
        raise HTTPException(status_code=404, detail="Product type not found")
    return product_type

async def get_bot(bot_id: int) -> Bot:
    bot: Union[Bot, None] = await session.get(Bot, bot_id)
    if bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@router.get("/get-all-product-types/{bot_id}")
async def get_product_types(bot_id: int, authorization: str = Header(None)):
    bot = await get_bot(bot_id)
    is_bot_owner(authorization, bot)

    product_types = (await session.scalars(select(ProductType).where(ProductType.bot_id == bot_id))).all()
    return product_types

@router.get("/get-all-products/{product_type_id}")
async def get_products(product_type_id: int, authorization: str = Header(None)):
    product_type = await get_product_type(product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)
    products = (await session.scalars(select(Product).where(Product.product_type_id == product_type_id))).all()
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
async def delete_product(product_id: int, authorization: str = Header(None)):
    product = await get_product(product_id)
    product_type = await get_product_type(product.product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)
    await session.delete(product)
    await session.commit()

@router.delete("/delete-product-type/{product_type_id}")
async def delete_product_type(product_type_id: int, authorization: str = Header(None)):
    product_type = await get_product_type(product_type_id)
    bot = await get_bot(product_type.bot_id)
    is_bot_owner(authorization, bot)

    dialogs = json.loads(bot.data_json)
    for dialog_key, dialog_value in dialogs["dialogs"].items():
        for stage_key, stage_value in dialog_value["stages"].items():
            if stage_value["type"] == "product":
                if product_type.name == stage_value["product"]["title"]:
                    raise HTTPException(status_code=400, detail="Delete product from bot first")
    await session.delete(product_type)
    await session.commit()
