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
