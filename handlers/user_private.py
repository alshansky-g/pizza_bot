from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, or_f
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from filters.chat_types import ChatTypeFilter
from keyboards import reply

router = Router()
router.message.filter(ChatTypeFilter(chat_types=["private"]))


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text='Привет, я виртуальный помощник',
                         reply_markup=reply.start_kb.as_markup(
                             resize_keyboard=True, one_time_keyboard=True
                         ))


@router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer(text="Вот меню:")


@router.message(or_f(Command("shipping"), F.text.lower().contains("доставк")))
async def logistics_info(message: types.Message):
    await message.answer(text="Доставляем быстро и качественно",
                         reply_markup=reply.contacts_kb)


@router.message(F.text.lower() == "варианты оплаты")
async def payment_options(message: types.Message):
    text = as_list(as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении: карта/наличные",
        "В заведении",
        marker="✅"
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Почта",
            "Голуби",
            marker="❌"
        ),
        sep="\n--------------\n")
    await message.answer(text=text.as_html())


@router.message(F.location)
async def get_contact(message: types.Message):
    await message.answer("Локация получена")
    await message.answer(str(message.location))


@router.message(F.contact)
async def get_location(message: types.Message):
    if message.contact:
        await message.answer("Номер телефона получен")
        await message.answer(str(message.contact.phone_number))
