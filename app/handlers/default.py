from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards import main_kb

default_router = Router()


@default_router.message(CommandStart())
async def cmd_start(message: Message):
    # logger.info(f"User upserted: {user_data['tg_user_id']} (ref={user_data['referral_link']})")
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=main_kb()
    )
