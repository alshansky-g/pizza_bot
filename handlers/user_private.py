from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import (
    decrease_items_in_cart,
    orm_add_to_cart,
    orm_add_user,
    orm_delete_from_cart,
)
from filters.custom import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from keyboards.inline import MenuCallback

router = Router()
router.message.filter(ChatTypeFilter(chat_types=['private']))


@router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name='Главная')
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@router.callback_query(MenuCallback.filter())
async def user_menu(callback: CallbackQuery, callback_data: MenuCallback, session: AsyncSession):
    menu_name = callback_data.menu_name

    if menu_name == 'В корзину':
        quantity = await add_to_cart(callback, callback_data, session)
        await callback.answer(f'Добавлено в корзину. Всего {quantity}')
        return
    elif menu_name == 'decrease':
        quantity = await decrease_items_in_cart(
            session, callback.from_user.id, callback_data.product_id
        )
        await callback.answer(f'В корзине: {quantity}')
    elif menu_name == 'delete':
        await orm_delete_from_cart(session, callback.from_user.id, callback_data.product_id)
        await callback.answer('Позиция удалена')

    media, reply_markup = await get_menu_content(
        session=session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


async def add_to_cart(callback: CallbackQuery, callback_data: MenuCallback, session: AsyncSession):
    await orm_add_user(
        session=session,
        user_id=callback.from_user.id,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name,
    )
    amount = await orm_add_to_cart(session, callback.from_user.id, callback_data.product_id)
    await session.commit()
    return amount
