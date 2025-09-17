# infra/repository/subscription.py
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update, delete, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from infra.models.subscription import Subscription
from infra.models.user import TelegramUser
from infra.repository.base import BaseRepo
from infra.shema.subscription import SubscriptionShema, SubscriptionUpdateShema


class SubscriptionRepo(BaseRepo):
    class SubscriptionRepo(BaseRepo):
        async def create_subscription(self, subscription: SubscriptionShema) -> Subscription:
            """
            Запись 1:1.ValueError, если для user_id уже есть подписка.
            """
            stmt = (
                insert(Subscription)
                .values(
                    id=subscription.user_id,
                    vpn_id=subscription.vpn_id,
                    vpn_key=subscription.vpn_key,
                    subscription_date=subscription.subscription_date or func.now(),
                    traffic=subscription.traffic,
                )
                .returning(Subscription)
            )
            try:
                res = await self.db_session.execute(stmt)
                obj = res.scalar_one()
                await self.db_session.commit()
                return obj
            except IntegrityError as e:
                await self.db_session.rollback()
                raise ValueError(f"Subscription already exists or FK constraint failed. Error text {e}")

        async def update_subscription(self, user_id: int, subscription: SubscriptionUpdateShema) -> Subscription | None:
            values = {k: v for k, v in subscription.model_dump(exclude_unset=True).items()}
            if not values:
                res = await self.db_session.execute(select(Subscription).where(Subscription.id == user_id))
                return res.scalar_one_or_none()
            stmt = (
                update(Subscription)
                .where(Subscription.id == user_id)
                .values(**values)
                .returning(Subscription)
            )
            res = await self.db_session.execute(stmt)
            obj = res.scalar_one_or_none()
            await self.db_session.commit()
            return obj

        async def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
            res = await self.db_session.execute(
                select(Subscription).where(Subscription.id == user_id)
            )
            return res.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        res = await self.db_session.execute(
            select(Subscription).where(Subscription.id == user_id)
        )
        return res.scalar_one_or_none()

    async def get_by_tg_user_id(self, tg_user_id: int) -> Optional[Subscription]:
        res = await self.db_session.execute(
            select(Subscription)
            .join(TelegramUser, TelegramUser.id == Subscription.id)
            .where(TelegramUser.tg_user_id == tg_user_id)
        )
        return res.scalar_one_or_none()

    async def set_vpn(
            self, user_id: int, *, vpn_id: uuid.UUID, vpn_key: Optional[str] = None
    ) -> None:
        values = {"vpn_id": vpn_id}
        if vpn_key is not None:
            values["vpn_key"] = vpn_key
        await self.db_session.execute(
            update(Subscription).where(Subscription.id == user_id).values(**values)
        )
        await self.db_session.commit()

    async def set_subscription_date(self, user_id: int, when: datetime) -> None:
        await self.db_session.execute(
            update(Subscription)
            .where(Subscription.id == user_id)
            .values(subscription_date=when)
        )
        await self.db_session.commit()

    async def delete_by_user_id(self, user_id: int) -> None:
        await self.db_session.execute(
            delete(Subscription).where(Subscription.id == user_id)
        )
        await self.db_session.commit()
