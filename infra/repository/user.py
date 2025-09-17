from typing import Optional
from sqlalchemy import case, literal
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func
from sqlalchemy import select

from infra.models.user import TelegramUser
from infra.repository.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        referral_link: Optional[str] = None,
    ):
        if referral_link is None:
            referral_link = "start"

        insert_values = {
            "tg_user_id": user_id,
            "username": username,
            "last_name": last_name,
            "first_name": first_name,
            "referral_link": referral_link,
        }

        stmt = insert(TelegramUser).values(**insert_values)
        ex = stmt.excluded

        upsert = (
            stmt.on_conflict_do_update(
                index_elements=[TelegramUser.tg_user_id],
                set_={
                    # не перезатираем существующие значения None-ами
                    "username": func.coalesce(ex.username, TelegramUser.username),
                    "last_name": func.coalesce(ex.last_name, TelegramUser.last_name),
                    "first_name": func.coalesce(ex.first_name, TelegramUser.first_name),

                    # обновляем referral_link только если в БД сейчас "start"
                    "referral_link": case(
                        (TelegramUser.referral_link == literal("start"),
                         func.coalesce(ex.referral_link, TelegramUser.referral_link)),
                        else_=TelegramUser.referral_link,
                    ),
                },
            )
            .returning(TelegramUser)
        )

        res = await self.db_session.execute(upsert)
        user = res.scalar_one()
        await self.db_session.commit()
        return user
