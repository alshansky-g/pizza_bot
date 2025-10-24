from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import (
    orm_get_banner,
    orm_get_categories,
    orm_get_products,
    orm_get_user_products,
)
from keyboards.inline import (
    empty_cart_kb,
    get_cart_buttons,
    get_products_btns,
    get_user_catalog_btns,
    main_menu_kb,
)
from utils.logging_config import logger
from utils.paginator import Paginator


async def main_menu(session: AsyncSession, menu_name: str):
    banner = await orm_get_banner(session, menu_name)
    media = InputMediaPhoto(media=banner.image, caption=banner.description)
    keyboard = main_menu_kb
    return media, keyboard


async def catalog(session: AsyncSession, level: int, menu_name: str):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    categories = await orm_get_categories(session)
    keyboard = get_user_catalog_btns(level=level, categories=categories)
    return image, keyboard


async def products(session: AsyncSession, level: int, category: int, page: int):
    products = await orm_get_products(session, category)
    paginator = Paginator(products, page=page)
    logger.debug(paginator.array)
    product, *_ = paginator.get_page()
    image = InputMediaPhoto(
        media=product.image,
        caption=f'<strong>{product.name}</strong>\n{product.description}\n'
        f'Стоимость: {round(product.price, 2)}\n'
        f'<strong>Товар {paginator.page} из {paginator.pages}</strong>',
    )
    pagination_buttons = paginator.get_buttons()
    keyboard = get_products_btns(
        level=level,
        category=category,
        page=page,
        pagination_btns=pagination_buttons,
        product_id=product.id,
    )
    return image, keyboard


async def cart(session, level, user_id, page, menu_name):
    user_cart = await orm_get_user_products(session, user_id)
    keyboard = empty_cart_kb
    if user_cart:
        products = [(pos.product, pos.quantity) for pos in user_cart]
        total_cost = sum(product.price * quantity for product, quantity in products)
        paginator = Paginator(products, page=page)
        cart, *_ = paginator.get_page()
        product, quantity = cart
        media = InputMediaPhoto(
            media=product.image,
            caption=f'<strong>{product.name}: {quantity} x {product.price} = '
            f'{product.price * quantity}</strong>\n'
            f'Позиций в корзине: <strong>{len(products)}</strong>\n'
            f'Общая стоимость заказа: <strong>{total_cost}</strong>',
        )
        pagination_buttons = paginator.get_buttons()
        keyboard = get_cart_buttons(
            level=level,
            pagination_btns=pagination_buttons,
            page=page,
            product_id=product.id,
            quantity=quantity,
        )
    if not user_cart:
        banner = await orm_get_banner(session, menu_name)
        media = InputMediaPhoto(media=banner.image, caption='Корзина пуста')
    return media, keyboard


async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    category: int | None = None,
    page: int | None = None,
    user_id: int | None = None,
):
    if level == 0:
        return await main_menu(session, menu_name)
    elif level == 1:
        return await catalog(session, level, menu_name)
    elif level == 2:
        return await products(session, level, category, page)
    elif level == 3:
        return await cart(session, level, user_id, page, menu_name)
