from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Banner, Cart, CartProduct, Category, Product, User


# Баннеры
async def orm_add_banner_description(session: AsyncSession, data: dict):
    banner = await session.scalar(select(Banner))
    if banner is None:
        session.add_all(
            [Banner(name=name, description=description) for name, description in data.items()]
        )
        await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    await session.execute(update(Banner).where(Banner.name == name).values(image=image))
    await session.commit()


async def orm_get_banner(session: AsyncSession, name: str):
    banner = await session.scalar(select(Banner).where(Banner.name == name))
    return banner


async def orm_get_info_pages(session: AsyncSession):
    pages_info = await session.scalars(select(Banner))
    return pages_info.all()


# Категории
async def orm_create_categories(session: AsyncSession, categories: list):
    category = await session.scalar(select(Category))
    if category is None:
        session.add_all([Category(name=name) for name in categories])
        await session.commit()


async def orm_get_categories(session: AsyncSession):
    categories = await session.scalars(select(Category))
    return categories.all()


# Админка Товары
async def orm_add_product(session: AsyncSession, product_fields: dict):
    product = Product(**product_fields)
    session.add(product)
    await session.commit()


async def orm_get_products(session: AsyncSession, category_id: int):
    products = await session.scalars(select(Product).where(Product.category_id == category_id))
    return products.all()


async def orm_get_product(session: AsyncSession, product_id: int):
    product = await session.get(Product, product_id)
    return product


async def orm_update_product(session: AsyncSession, product_id: int, data: dict):
    await session.execute(
        update(Product)
        .where(Product.id == product_id)
        .values(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image=data['image'],
        )
    )
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    await session.execute(delete(Product).where(Product.id == product_id))
    await session.commit()


# Создание пользователя
async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
):
    user = await session.get(User, user_id)
    if user is None:
        user = User(id=user_id, first_name=first_name, last_name=last_name, phone=phone)
        user.cart = Cart(id=user_id)
        session.add(user)
        # await session.commit()


# Работа с корзиной
async def orm_add_to_cart(session: AsyncSession, user_id: int, product_id: int):
    cart = await session.get(CartProduct, (product_id, user_id))
    amount = 1
    if cart:
        cart.quantity += 1
        amount = cart.quantity
    else:
        session.add(CartProduct(cart_id=user_id, product_id=product_id, quantity=1))
    return amount


async def orm_get_user_products(session: AsyncSession, user_id: int):
    query = (
        select(User)
        .options(
            joinedload(User.cart).joinedload(Cart.products_assoc).joinedload(CartProduct.product)
        )
        .where(User.id == user_id)
    )
    user = await session.scalar(query)
    return user.cart.products


async def orm_delete_from_cart(session: AsyncSession, user_id: int, product_id: int):
    await session.execute(
        delete(CartProduct).where(
            CartProduct.cart_id == user_id, CartProduct.product_id == product_id
        )
    )
    await session.commit()


async def decrease_items_in_cart(session: AsyncSession, user_id: int, product_id: int):
    product = await session.scalar(
        select(CartProduct).where(
            CartProduct.cart_id == user_id, CartProduct.product_id == product_id
        )
    )
    if product is None:
        return
    if product.quantity > 1:
        product.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        return False
