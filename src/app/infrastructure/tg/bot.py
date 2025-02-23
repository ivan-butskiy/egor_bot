import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.app.entrypoints.tg import router as base_router
from src.suppliers.entrypoints.tg import router as suppliers_router
from src.users.entrypoints.tg import router as users_router
from src.orders.entrypoints.tg import router as orders_router


bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dispatcher = Dispatcher()


dispatcher.include_routers(
    base_router,
    users_router,
    suppliers_router,
    orders_router
)
