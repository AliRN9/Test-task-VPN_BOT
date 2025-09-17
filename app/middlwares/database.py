from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from infra import get_db_session
from infra.repository.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool=get_db_session) -> None:
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        referral = "start"

        if isinstance(event, Message):
            if event.text.startswith("/start"):
                parts = event.text.split(maxsplit=1)
                referral = parts[1].strip() if len(parts) == 2 else "start"

        async with self.session_pool() as session:
            repo = RequestsRepo(session)
            user = await repo.users.get_or_create_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.first_name,
                event.from_user.last_name,
                referral
            )

            # прокидываем зависимости
            data["repo"] = repo
            data["user"] = user

            # data["db_session"] = self.session_pool  # если где-то ещё нужно открыть сессию вручную

            return await handler(event, data)
