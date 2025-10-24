from collections.abc import Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Category


class MenuCallback(CallbackData, prefix='menu'):
    level: int
    menu_name: str | None = None
    category: int | None = None
    page: int = 1
    product_id: int | None = None


empty_cart_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Назад', callback_data=MenuCallback(level=0, menu_name='Главная').pack()
            )
        ]
    ]
)

main_menu_kb = (
    InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(
                    text='Товары 🍕',
                    callback_data=MenuCallback(level=1, menu_name='Категории').pack(),
                ),
                InlineKeyboardButton(
                    text='Корзина 🛒',
                    callback_data=MenuCallback(level=3, menu_name='Корзина').pack(),
                ),
                InlineKeyboardButton(
                    text='О нас ℹ️', callback_data=MenuCallback(level=0, menu_name='О нас').pack()
                ),
                InlineKeyboardButton(
                    text='Оплата 💳', callback_data=MenuCallback(level=0, menu_name='Оплата').pack()
                ),
                InlineKeyboardButton(
                    text='Доставка 🚗',
                    callback_data=MenuCallback(level=0, menu_name='Доставка').pack(),
                ),
            ]
        ]
    )
    .adjust(2)
    .as_markup()
)


def get_user_catalog_btns(
    *, level: int, categories: Sequence[Category], adjust_values: tuple[int, ...] = (2,)
):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='Назад', callback_data=MenuCallback(level=level - 1, menu_name='Главная').pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Корзина 🛒', callback_data=MenuCallback(level=3, menu_name='Корзина').pack()
        )
    )

    for cat in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=cat.name,
                callback_data=MenuCallback(
                    level=level + 1, menu_name=cat.name, category=cat.id
                ).pack(),
            )
        )
    return keyboard.adjust(*adjust_values).as_markup()


def get_products_btns(
    *,
    level: int,
    category: int,
    page: int,
    pagination_btns: dict,
    product_id: int,
    adjust_values: tuple[int, ...] = (2, 1),
):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='Назад', callback_data=MenuCallback(level=level - 1, menu_name='Категории').pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Корзина 🛒', callback_data=MenuCallback(level=3, menu_name='Корзина').pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Купить 💸',
            callback_data=MenuCallback(
                level=level, menu_name='В корзину', product_id=product_id, category=category
            ).pack(),
        )
    )
    keyboard.adjust(*adjust_values)

    row = []
    for text, menu_name in pagination_btns.items():
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallback(
                    level=level,
                    menu_name=menu_name,
                    category=category,
                    page=page + 1 if menu_name == 'next' else page - 1,
                ).pack(),
            )
        )

    return keyboard.row(*row).as_markup()


def get_cart_buttons(*, level, page, pagination_btns, product_id, quantity):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='-1',
            callback_data=MenuCallback(
                level=level, menu_name='decrease', product_id=product_id, page=page
            ).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='+1',
            callback_data=MenuCallback(
                level=level, menu_name='В корзину', product_id=product_id, page=page
            ).pack(),
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Удалить',
            callback_data=MenuCallback(
                level=level, menu_name='delete', product_id=product_id, page=page
            ).pack(),
        )
    )
    row = []
    for text, menu_name in pagination_btns.items():
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallback(
                    level=level,
                    menu_name=menu_name,
                    page=page + 1 if menu_name == 'next' else page - 1,
                ).pack(),
            )
        )
    keyboard = keyboard.row(*row)
    keyboard.row(
        InlineKeyboardButton(
            text='Назад', callback_data=MenuCallback(level=1, menu_name='Категории').pack()
        )
    )
    return keyboard.as_markup()


def get_inline_kbd(*, buttons: dict[str, str], adjust_values: tuple[int, ...] = (2,)):
    keyboard = InlineKeyboardBuilder()
    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*adjust_values).as_markup()
