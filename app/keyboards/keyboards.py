from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать пользователя", callback_data="create_user")],
        [InlineKeyboardButton(text="Получить ключ", callback_data="get_key")],
        [InlineKeyboardButton(text="Продлить ключ", callback_data="renew_key")],
    ])

