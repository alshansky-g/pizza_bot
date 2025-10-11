from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard

router = Router()
router.message.filter(ChatTypeFilter(chat_types=["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Посмотреть список товаров",
    placeholder="Выберите действие",
    adjust_values=(2, 1, 1)
)


@router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@router.message(F.text == "Посмотреть список товаров")
async def get_products(message: types.Message):
    await message.answer(text="Список товаров:")


@router.message(F.text == "Изменить товар")
async def update_product(message: types.Message):
    await message.answer("Обновляем товар...")


@router.message(F.text == "Удалить товар")
async def delete_product(message: types.Message):
    await message.answer("Удаляем товар...")


# FSM related
@router.message(F.text == "Добавить товар")
async def create_product(message: types.Message):
    await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())


@router.message(Command("отмена"))
@router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message):
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@router.message(Command("назад"))
@router.message(F.text.casefold() == "назад")
async def back_handler(message: types.Message):
    await message.answer("Вы вернулись к прошлому шагу")


@router.message(F.text)
async def add_name(message: types.Message):
    await message.answer("Введите описание товара")


@router.message(F.text)
async def add_description(message: types.Message):
    await message.answer("Введите стоимость товара")


@router.message(F.text)
async def add_price(message: types.Message):
    await message.answer("Загрузите изображение товара")


@router.message(F.text)
async def add_image(message: types.Message):
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
