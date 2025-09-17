from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards import main_kb
from infra import get_db_session
from test.add_subscriptions import add_mocs_subscriptions

test_router = Router()


@test_router.message(Command("add_mocs_subscription"))
async def cmd_start(message: Message):
    async with get_db_session() as session:
        await add_mocs_subscriptions(session)
    await message.answer(
        "Добавлены тестовые подписки",
        reply_markup=main_kb()
    )
