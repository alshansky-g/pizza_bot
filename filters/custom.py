from aiogram.filters import Filter
from aiogram.types import Message


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    async def __call__(self, message: Message, admins_list: list[int]) -> bool:
        if message.from_user:
            return message.from_user.id in admins_list
        return False


class ProductId(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            return message.text.isalnum()
        return False
