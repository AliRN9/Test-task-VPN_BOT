import asyncio
import logging
import logging.config
import os

import yaml
from aiogram import Dispatcher

from app.handlers import routers_list
from app.middlwares.database import DatabaseMiddleware
from bot import bot
from infra import get_db_session


def setup_logging(config_path: str = "config/logging.conf.yml") -> None:
    os.makedirs("logs", exist_ok=True)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)


def register_global_middlewares(dp: Dispatcher, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        DatabaseMiddleware(session_pool),

    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


async def main() -> None:
    setup_logging()
    logger = logging.getLogger('vpn_service')
    logger.info("Starting vpn_service bot")
    dp = Dispatcher()
    register_global_middlewares(dp, get_db_session)
    dp.include_routers(*routers_list)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
