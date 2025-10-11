from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.reply import get_keyboard
from utils.logging_config import logger

router = Router()
router.message.filter(ChatTypeFilter(chat_types=["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Посмотреть список товаров",
    placeholder="Выберите действие",
    adjust_values=(2, 1, 1),
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
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        "AddProduct:name": "Введите название:",
        "AddProduct:description": "Введите описание:",
        "AddProduct:price": "Введите стоимость:",
        "AddProduct:image": "Добавьте изображение:",
    }


@router.message(StateFilter(None), F.text == "Добавить товар")
async def create_product(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)


@router.message(StateFilter("*"), Command("отмена"))
@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@router.message(StateFilter("*"), Command("назад"))
@router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет. Введите название товара или напишите "отмена"')
        return
    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Вы вернулись к предыдущему шагу\n{AddProduct.texts[previous.state]}"  # type: ignore
            )
            return
        previous = step


@router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара:")
    await state.set_state(AddProduct.description)


@router.message(AddProduct.name)
async def add_name_fallback(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Введите название товара:")


@router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара:")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.description)
async def add_description_fallback(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Введите описание товара:")


@router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара:")
    await state.set_state(AddProduct.image)


@router.message(AddProduct.price)
async def add_price_fallback(message: types.Message):
    await message.answer("Вы ввели недопустимые данные. Введите стоимость товара:")


@router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
        logger.debug("Добавленный товар: {}", await state.get_data())
        await state.clear()


@router.message(AddProduct.image)
async def add_image_fallback(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные. Загрузите изображение товара:")
