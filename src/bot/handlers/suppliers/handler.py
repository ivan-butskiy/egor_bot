from aiogram import Router, F
from aiogram import types

from src.domain.suppliers import views
from src.domain.suppliers.bootstrap import bootstrap as suppliers_bootstrap
from src.domain.users import User
from src.bot.handlers.utils import auth_decorator
from src.bot.handlers.base import commands as base_cmd
from src.bot.handlers.base.keyboards import get_start_keyboard
from . import keyboards as kb
from . import commands as cmd


suppliers_router = Router()
suppliers_bootstrap = suppliers_bootstrap()


@suppliers_router.message(F.text == base_cmd.StartKbCommands.suppliers)
@auth_decorator
async def handle_suppliers(message: types.Message, user: User):
    count = await views.get_suppliers_count(suppliers_bootstrap.uow)
    if not user.is_admin and not count:
        markup = get_start_keyboard(user)
        text = 'Наразі немає жодного постачальника. Оберіть дію'
    else:
        text = 'Оберіть дію'
        markup = kb.get_suppliers_keyboard(count)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@suppliers_router.message(F.text == cmd.SuppliersCommands.get_suppliers)
@auth_decorator
async def handle_get_suppliers(message: types.Message, user: User):
    items = await views.get_suppliers(0, 10, suppliers_bootstrap.uow)
    markup = kb.get_list_suppliers_list_keyboard(items=items, user=user)
    await message.answer(
        text='Оберіть постачальника:',
        reply_markup=markup
    )
