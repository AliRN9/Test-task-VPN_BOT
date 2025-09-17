import logging
from datetime import datetime, timezone, timedelta

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.exceptions import RemnawaveError
from app.service.remnawave.remnawave import RemnawaveClient
from infra.models import TelegramUser
from infra.repository.requests import RequestsRepo
from settings import settings

logger = logging.getLogger("vpn_service")

remnawave_router = Router()

client = RemnawaveClient(api_token=settings.REMNAWAVE_SECRET_TOKEN)


@remnawave_router.callback_query(F.data == "create_user")
async def cb_create_user(callback: CallbackQuery, repo: RequestsRepo, user: TelegramUser):
    tg_id = callback.from_user.id
    logger.info(f"start created user")

    try:
        created = await client.create_user(
            username=user.username,
            created_at=datetime.now(timezone.utc),
            expire_at=datetime.now(timezone.utc) + timedelta(days=7),
            description=f"created by bot for {user.first_name} {user.last_name}",
            tag="telegram",
            telegram_id=tg_id
        )

    except RemnawaveError as e:
        await callback.message.answer(f"Remnawave ошибка ({e.status}): {e.detail}")

    else:
        logger.info(f"created user: {created}")

        # logger.info(f"Created key for {tg_id}: {created['vpn_id']} expires {created['expires_at']}")

        await callback.message.answer(
            f"Ключ создан!\\nСсылка на подписку: https://vpn.com:{user.tg_user_id}/sub\\nДействует до: {created['expires_at'].strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )
        await callback.answer()

#
# @remnawave_router.callback_query(F.data == "get_key")
# async def cb_get_key(callback: CallbackQuery):
#     tg_id = callback.from_user.id
#     sub = await get_latest_subscription(tg_id)
#     if not sub:
#         await callback.message.answer("Подписка не найдена. Нажмите «Создать пользователя».")
#         await callback.answer()
#         return
#     expires_at = sub["expires_at"]
#     if isinstance(expires_at, datetime):
#         expires_str = expires_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
#     else:
#         expires_str = str(expires_at)
#     await callback.message.answer(
#         f"Ваша ссылка на подписку: {sub['vpn_key']}\\nПодписка действует до: {expires_str}"
#     )
#     await callback.answer()
#
#
# @remnawave_router.callback_query(F.data == "renew_key")
# async def cb_renew_key(callback: CallbackQuery):
#     tg_id = callback.from_user.id
#     sub = await get_latest_subscription(tg_id)
#     if not sub:
#         await callback.message.answer("Подписка не найдена. Нажмите «Создать пользователя».")
#         await callback.answer()
#         return
#     renewed = await client.renew_key(sub["vpn_id"], days=settings.subscription_days)
#     await update_subscription_expiry(tg_id, sub["vpn_id"], renewed["expires_at"])
#     await callback.message.answer(
#         f"Подписка продлена до: {renewed['expires_at'].strftime('%Y-%m-%d %H:%M:%S %Z')}"
#     )
#     await callback.answer()
