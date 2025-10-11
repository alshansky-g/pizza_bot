from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, or_f
from filters.chat_types import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(chat_types=["private"]))


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text='Привет, я виртуальный помощник')


@router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer(text="Вот меню:")


@router.message(or_f(Command("shipping"), F.text.lower().contains("доставк")))
async def logistics_info(message: types.Message):
    await message.answer(text="Доставляем быстро и качественно")
