from aiogram import Dispatcher

from src.bot import handlers


def setup_routers(dispatcher: Dispatcher):
    dispatcher.include_router(handlers.base_router)
    dispatcher.include_router(handlers.users_router)
