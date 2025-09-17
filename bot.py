from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from settings import settings


bot = Bot(token=settings.BotToken, default=DefaultBotProperties(parse_mode=ParseMode.HTML))