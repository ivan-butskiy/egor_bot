from aiogram import Router, F
from aiogram import types

from src.bot.handlers.utils import auth_decorator
from src.domain.suppliers import views
from src.domain.suppliers.bootstrap import bootstrap as suppliers_bootstrap


suppliers_router = Router()
suppliers_bootstrap = suppliers_bootstrap()


@suppliers_router.message(F.text == 'Постачальники')
@auth_decorator
async def handle_suppliers(message: types.Message):
    suppliers = await views.get_suppliers(0, 10, suppliers_bootstrap.uow)
    await message.answer(text='Foo bar')
