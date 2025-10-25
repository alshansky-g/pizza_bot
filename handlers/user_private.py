from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from filters.custom import ChatTypeFilter
from handlers.menu_processing import get_menu_content, process_cart_actions
from keyboards.inline import MenuCallback

router = Router()
router.message.filter(ChatTypeFilter(chat_types=['private']))


@router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name='Главная')
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@router.callback_query(MenuCallback.filter())
async def user_menu(callback: CallbackQuery, callback_data: MenuCallback, session: AsyncSession):
    quantity = await process_cart_actions(callback, callback_data, session)
    page = (
        callback_data.page - 1 if (not quantity and callback_data.page > 1) else callback_data.page
    )
    media, reply_markup = await get_menu_content(
        session=session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=page,
        user_id=callback.from_user.id,
    )
    if media.caption == callback.message.html_text:
        await callback.answer()
        return
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
