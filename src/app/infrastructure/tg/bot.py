import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.app.entrypoints.tg import router as base_router
from src.suppliers.entrypoints.tg import router as suppliers_router
from src.users.entrypoints.tg import router as users_router


bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dispatcher = Dispatcher()


dispatcher.include_router(base_router)
dispatcher.include_router(users_router)
dispatcher.include_router(suppliers_router)
