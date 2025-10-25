from aiogram.types import CallbackQuery, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database import crud
from keyboards import inline
from utils.paginator import Paginator


async def main_menu(session: AsyncSession, menu_name: str):
    banner = await crud.orm_get_banner(session, menu_name)
    media = InputMediaPhoto(media=banner.image, caption=banner.description)
    keyboard = inline.main_menu_kb
    return media, keyboard


async def catalog(session: AsyncSession, level: int, menu_name: str):
    banner = await crud.orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    categories = await crud.orm_get_categories(session)
    keyboard = inline.get_user_catalog_btns(level=level, categories=categories)
    return image, keyboard


async def products(session: AsyncSession, level: int, category: int, page: int):
    products = await crud.orm_get_products(session, category)
    paginator = Paginator(products, page=page)
    product, *_ = paginator.get_page()
    image = InputMediaPhoto(
        media=product.image,
        caption=f'<b>{product.name}</b>\n{product.description}\n'
        f'Стоимость: {round(product.price, 2)}\n'
        f'<b>Товар {paginator.page} из {paginator.pages}</b>',
    )
    pagination_buttons = paginator.get_buttons()
    keyboard = inline.get_products_btns(
        level=level,
        category=category,
        page=page,
        pagination_btns=pagination_buttons,
        product_id=product.id,
    )
    return image, keyboard


async def cart(session: AsyncSession, level: int, user_id: int, page: int):
    user_cart = await crud.orm_get_user_products(session, user_id)
    keyboard = inline.empty_cart_kb
    if user_cart:
        products = [(pos.product, pos.quantity) for pos in user_cart]
        total_cost = sum(product.price * quantity for product, quantity in products)
        paginator = Paginator(products, page=page)
        cart, *_ = paginator.get_page()
        product, quantity = cart
        media = InputMediaPhoto(
            media=product.image,
            caption=f'<b>{product.name}: {quantity} x {product.price} = '
            f'{product.price * quantity}</b>\n'
            f'Позиций в корзине: <b>{len(products)}</b>\n'
            f'Общая стоимость заказа: <b>{total_cost}</b>',
        )
        pagination_buttons = paginator.get_buttons()
        keyboard = inline.get_cart_buttons(
            level=level,
            pagination_btns=pagination_buttons,
            page=page,
            product_id=product.id,
        )
    if not user_cart:
        banner = await crud.orm_get_banner(session, name='Корзина')
        media = InputMediaPhoto(media=banner.image, caption='Корзина пуста')
    return media, keyboard


async def process_cart_actions(
    callback: CallbackQuery,
    callback_data: inline.MenuCallback,
    session: AsyncSession,
    quantity: int = 1,
):
    menu_name = callback_data.menu_name
    if menu_name == 'add_to_cart':
        quantity = await add_to_cart(callback, callback_data, session)
        await callback.answer(f'В корзине: {quantity}')
    elif menu_name == 'decrease':
        quantity = await crud.decrease_items_in_cart(
            session, callback.from_user.id, callback_data.product_id
        )
        await callback.answer(f'В корзине: {quantity}')
    elif menu_name == 'delete':
        quantity = await crud.orm_delete_from_cart(
            session, callback.from_user.id, callback_data.product_id
        )
        await callback.answer('Позиция удалена')
    return quantity


async def add_to_cart(
    callback: CallbackQuery, callback_data: inline.MenuCallback, session: AsyncSession
):
    await crud.orm_add_user(
        session=session,
        user_id=callback.from_user.id,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name,
    )
    amount = await crud.orm_add_to_cart(session, callback.from_user.id, callback_data.product_id)
    await session.commit()
    return amount


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
        return await cart(session, level, user_id, page)
