from database.models import Product
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def orm_add_product(session: AsyncSession, product_fields: dict):
    product = Product(**product_fields)
    session.add(product)
    await session.commit()


async def orm_get_products(session: AsyncSession):
    products = await session.scalars(select(Product))
    return products.all()


async def orm_get_product(session: AsyncSession, product_id: int):
    product = await session.get(Product, product_id)
    return product


async def orm_update_product(session: AsyncSession, product_id: int, data: dict):
    await session.execute(
        update(Product).where(Product.id == product_id).values(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            image=data["image"]
        ))
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    await session.execute(delete(Product).where(Product.id == product_id))
    await session.commit()
