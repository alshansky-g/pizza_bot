from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


class MenuCallback(CallbackData, prefix='menu'):
    level: int
    menu_name: str


def get_user_main_btns(*, level: int, adjust_values: tuple[int, ...] | None = (2,)):
    keyboard = InlineKeyboardBuilder()
    buttons = {
        'Товары 🍕': 'catalog',
        'Корзина 🛒': 'cart',
        'О нас ℹ️': 'about',
        'Оплата 💳': 'payment',
        'Доставка 🚗': 'shipping'
    }
    for text, menu_name in buttons.items():
        if menu_name == 'catalog':
            keyboard.add(InlineKeyboardButton(
                text=text, callback_data=MenuCallback(
                    level=level + 1, menu_name=menu_name).pack()))
        elif menu_name == 'cart':
            keyboard.add(InlineKeyboardButton(
                text=text, callback_data=MenuCallback(
                    level=3, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(
                text=text, callback_data=MenuCallback(
                    level=level, menu_name=menu_name).pack()))
    if adjust_values:
        keyboard.adjust(*adjust_values)

    return keyboard.as_markup()
