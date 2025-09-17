import logging
import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import select

from infra.models import TelegramUser
from infra.models.subscription import Subscription


async def add_mocs_subscriptions(session) -> None:
    TELEGRAM_USER_MOCKS = [
        {"tg_user_id": 1016218961, "username": "user1", "first_name": "Jon", "last_name": "R",
         "referral_link": "start"},
        {"tg_user_id": 555000111, "username": "user2", "first_name": "Bob", "last_name": "K",
         "referral_link": "gift_abc"},
        {"tg_user_id": 777888999, "username": "user3", "first_name": "Cat", "last_name": "Z", "referral_link": "start"},
    ]

    users = []
    for u in TELEGRAM_USER_MOCKS[1:]:
        obj = TelegramUser(**u)
        session.add(obj)
        users.append(obj)
    await session.flush()  # получаем users.id без коммита

    now = datetime.now(timezone.utc)
    my_user = await session.execute(select(TelegramUser).where(TelegramUser.tg_user_id == 1016218961))
    logging.info(f"{my_user=}")

    users.append(my_user.scalar_one())
    # 2) subscriptions, FK = users[i].id
    subs = [
        Subscription(
            id=users[0].id,
            vpn_key="https://vpn.example.com/sub/aa11bb22",
            vpn_id=uuid.uuid4(),
            subscription_date=now + timedelta(days=7),
            traffic=123_456,
        ),
        Subscription(
            id=users[1].id,
            vpn_key="https://vpn.example.com/sub/cc33dd44",
            vpn_id=uuid.uuid4(),
            subscription_date=now + timedelta(hours=12),
            traffic=0,
        ),
        Subscription(
            id=users[2].id,
            vpn_key="https://vpn.example.com/sub/ee55ff66",
            vpn_id=uuid.uuid4(),
            subscription_date=now + timedelta(hours=2),
            traffic=9_876_543,
        ),
    ]
    session.add_all(subs)
    await session.commit()
