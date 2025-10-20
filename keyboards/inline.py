from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallback(CallbackData, prefix='menu'):
    level: int
    menu_name: str
    category: int | None = None


def get_user_main_btns(*, level: int, adjust_values: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    buttons = {
        'Товары 🍕': 'Категории',
        'Корзина 🛒': 'Корзина',
        'О нас ℹ️': 'О нас',
        'Оплата 💳': 'Оплата',
        'Доставка 🚗': 'Доставка'
    }
    for text, menu_name in buttons.items():
        if menu_name == 'Категории':
            keyboard.add(InlineKeyboardButton(
                text=text, callback_data=MenuCallback(
                    level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'Корзина':
            keyboard.add(InlineKeyboardButton(
                text=text, callback_data=MenuCallback(
                    level=3, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(
                text=text, callback_data=MenuCallback(
                    level=level, menu_name=menu_name).pack()))

    return keyboard.adjust(*adjust_values).as_markup()


def get_user_catalog_btns(*, level: int, categories: list, adjust_values: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text='Назад', callback_data=MenuCallback(
            level=level - 1, menu_name='Главная').pack()))
    keyboard.add(InlineKeyboardButton(
        text='Корзина 🛒', callback_data=MenuCallback(
            level=3, menu_name='Корзина').pack()))

    for cat in categories:
        keyboard.add(InlineKeyboardButton(
            text=cat.name, callback_data=MenuCallback(
                level=level + 1, menu_name=cat.name, category=cat.id).pack()))
    return keyboard.adjust(*adjust_values).as_markup()


def get_inline_kbd(
        *,
        buttons: dict[str, str],
        adjust_values: tuple[int, ...] | None = None
):
    keyboard = InlineKeyboardBuilder()
    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    if adjust_values:
        keyboard.adjust(*adjust_values)
    return keyboard.as_markup()
