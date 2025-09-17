from sqlalchemy import case, literal, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from infra.models.user import TelegramUser
from infra.repository.base import BaseRepo
from infra.shema.user import UserCreateShema


class UserRepo(BaseRepo):
    async def get_or_create_user(self, user: UserCreateShema):
        values = user.model_dump(exclude_unset=True)
        stmt = insert(TelegramUser).values(**values)
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

    async def get_user_by_tg_id(self, tg_user_id: int):
        res = await self.db_session.execute(
            select(TelegramUser).where(TelegramUser.tg_user_id == tg_user_id)
        )
        return res.scalar_one_or_none()
