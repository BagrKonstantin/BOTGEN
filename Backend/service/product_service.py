import json
from typing import Union

from fastapi import HTTPException
from sqlalchemy import select

from utils.config import session
from utils.models import Product, ProductType, Bot


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

async def get_product_types(bot_id: int):
    product_types = (await session.scalars(select(ProductType).where(ProductType.bot_id == bot_id))).all()
    return product_types

async def get_products(product_type_id):
    products = (await session.scalars(select(Product).where(Product.product_type_id == product_type_id))).all()
    return products



async def delete_product(product: Product):
    await session.delete(product)
    await session.commit()


async def delete_product_type(bot:Bot, product_type: ProductType):
    dialogs = json.loads(bot.data_json)
    for dialog_key, dialog_value in dialogs["dialogs"].items():
        for stage_key, stage_value in dialog_value["stages"].items():
            if stage_value["type"] == "product":
                if product_type.name == stage_value["product"]["title"]:
                    raise HTTPException(status_code=400, detail="Delete product from bot first")
    await session.delete(product_type)
    await session.commit()