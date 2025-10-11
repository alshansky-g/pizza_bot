from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardBuilder()
start_kb.add(
    KeyboardButton(text="Меню"),
    KeyboardButton(text="О магазине"),
    KeyboardButton(text="Варианты доставки"),
    KeyboardButton(text="Варианты оплаты"),
    KeyboardButton(text="Оставить отзыв"),
)
start_kb.adjust(2, 2, 1)

contacts_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер 📞", request_contact=True),
            KeyboardButton(text="Отправить геолокацию 🗺️", request_location=True),
        ],
    ],
    resize_keyboard=True,
)
