from database.models import Product
from sqlalchemy.ext.asyncio import AsyncSession


async def orm_add_product(session: AsyncSession, product_fields: dict):
    product = Product(**product_fields)
    session.add(product)
    await session.commit()
