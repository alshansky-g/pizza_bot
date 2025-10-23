from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.crud import orm_add_banner_description, orm_create_categories
from database.models import Base
from utils.config import config
from utils.db_texts import categories, info_pages_description

engine = create_async_engine(url=config.database_url, echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        await orm_create_categories(session, categories)
        await orm_add_banner_description(session, info_pages_description)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
