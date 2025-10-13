from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base
from utils.config import config

engine = create_async_engine(url=config.database_url, echo=True)
session_maker = async_sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
