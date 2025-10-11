from string import punctuation

from aiogram import Router, types
from filters.chat_types import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(chat_types=["group", "supergroup"]))

restricted_words = {"кабан", "хомяк", "выхухоль"}


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@router.edited_message()
@router.message()
async def cleaner(message: types.Message):
    assert message.text, "В сообщении должен быть текст"
    assert message.from_user

    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.reply(
            text=f"{message.from_user.first_name}, "
            "запрещено использовать оскорбления. Вас предупредили."
        )
        await message.delete()
        # await message.chat.ban(message.from_user.id)
    else:
        await message.answer(message.text)
