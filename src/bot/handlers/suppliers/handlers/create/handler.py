from aiogram import Router, F
from aiogram import types

from src.bot.handlers.suppliers import commands as suppliers_cmd
from src.bot.handlers.utils import auth_decorator


router = Router(name=__name__)


@router.message(F.text == suppliers_cmd.SuppliersCommands.create_supplier)
@auth_decorator
async def handle_create_supplier(message: types.Message):
    d = 1


async def handle_title(message: types.Message):
    pass
