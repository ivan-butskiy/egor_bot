from aiogram import Dispatcher

from src.app.entrypoints.tg import router as base_router
from src.suppliers.entrypoints.tg import router as suppliers_router
from src.users.entrypoints.tg import router as users_router


def setup_routers(dispatcher: Dispatcher):
    dispatcher.include_router(base_router)
    dispatcher.include_router(users_router)
    dispatcher.include_router(suppliers_router)
