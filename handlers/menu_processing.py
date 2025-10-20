from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import orm_get_banner
from keyboards.inline import get_user_main_btns


async def main_menu(session: AsyncSession, level: int, menu_name: str):
    banner = await orm_get_banner(session, menu_name)
    media = InputMediaPhoto(media=banner.image, caption=banner.description)
    keyboard = get_user_main_btns(level=level)
    return media, keyboard


# TODO дописать
async def get_menu_content(session: AsyncSession, level: int, menu_name: str):
    if level == 0:
        return await main_menu(session, level, menu_name)
