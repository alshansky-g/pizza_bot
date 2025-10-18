from aiogram.utils.formatting import Bold, as_list, as_marked_section

categories = ["Еда", "Напитки"]

info_pages_description = {
    "main": "Добро пожаловать",
    "about": "Пиццерия 'У братишки'\nРежим работы - 24/7",
    "payment": as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении: карта/наличные",
        "В заведении",
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варианты доставки^"),
            "Курьер",
            "Самовынос",
            marker="✅ "
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Почта",
            "Голуби",
            marker="❌ "
            ),
            sep="\n-------------------------------\n"
    ).as_html(),
    "catalog": "Категории:",
    "cart": "Корзина пуста."
}
