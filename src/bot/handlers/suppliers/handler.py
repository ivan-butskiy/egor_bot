from aiogram import Router, F
from aiogram import types
from aiogram import html

from src.domain.suppliers import views, Supplier
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
        markup = kb.get_suppliers_kb(count)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@suppliers_router.message(F.text == cmd.SuppliersCommands.get_suppliers)
@auth_decorator
async def handle_get_suppliers(message: types.Message, user: User):
    items, count = await views.get_suppliers(suppliers_bootstrap.uow, 0)
    markup = kb.get_suppliers_list_kb(items=items, count=count, user=user)
    await message.answer(
        text='Оберіть постачальника:',
        reply_markup=markup
    )


@suppliers_router.callback_query(F.data.startswith(cmd.SuppliersCallback.paginate_suppliers))
@auth_decorator
async def handle_paginate_suppliers(callback_query: types.CallbackQuery, user: User):
    page: int = int(callback_query.data.split('_')[-1])
    limit = 10
    items, count = await views.get_suppliers(suppliers_bootstrap.uow, (page - 1) * limit, limit)
    markup = kb.get_suppliers_list_kb(items=items, count=count, user=user, page=page)
    await callback_query.message.edit_text(
        text=f'Постачальники, сторінка {page}',
        reply_markup=markup
    )


@suppliers_router.callback_query(F.data.startswith(cmd.SuppliersCallback.supplier_item))
@auth_decorator
async def handle_supplier_item(callback_query: types.CallbackQuery, user: User):
    item_id: int = int(callback_query.data.split('_')[-1])
    supplier: Supplier = await views.get_supplier(suppliers_bootstrap.uow, item_id)

    if user.is_admin:
        text = f'{supplier.title} ({supplier.alias})'
    else:
        text = supplier.alias

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=html.bold(text),
        reply_markup=kb.get_supplier_item_kb(user)
    )
