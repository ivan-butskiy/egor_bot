from aiogram import Router, F
from aiogram import types
from aiogram import html

from src.users import User
from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import commands as base_cmd
from src.app.entrypoints.tg.handlers.keyboards import get_start_kb
from src.suppliers import views, Supplier
from src.suppliers.bootstrap import bootstrap
from src.suppliers.entrypoints.tg import commands as cmd, keyboards as kb
from src.suppliers.entrypoints.tg.filters import (
    SupplierItemFilter,
    PaginateSuppliersFilter,
    SupplierItemActionEnum
)
from .update import router as update_router
from .create import router as create_router
from .delete import router as delete_router


router = Router(name=__name__)


@router.message(F.text == base_cmd.StartKbCommands.suppliers)
@auth_decorator
async def handle_suppliers(message: types.Message, user: User):
    count = await views.get_suppliers_count(bootstrap.uow)
    if not user.is_admin and not count:
        markup = get_start_kb(user)
        text = 'Наразі немає жодного постачальника. Оберіть дію:'
    else:
        text = 'Оберіть дію:'
        markup = kb.get_suppliers_kb(count)
    await message.answer(
        text=text,
        reply_markup=markup
    )


@router.message(F.text == cmd.SuppliersCommands.get_suppliers)
@auth_decorator
async def handle_get_suppliers(message: types.Message, user: User):
    items, count = await views.get_suppliers(bootstrap.uow)
    markup = kb.get_suppliers_list_kb(items=items, count=count, user=user)
    await message.answer(
        text='Оберіть постачальника:',
        reply_markup=markup
    )


@router.callback_query(PaginateSuppliersFilter.filter())
@auth_decorator
async def handle_paginate_suppliers(
        callback_query: types.CallbackQuery,
        callback_data: PaginateSuppliersFilter,
        user: User
):
    page = callback_data.page
    limit = 10
    items, count = await views.get_suppliers(bootstrap.uow, (page - 1) * limit, limit)
    markup = kb.get_suppliers_list_kb(items=items, count=count, user=user, page=page)
    await callback_query.message.edit_text(
        text=f'Постачальники, сторінка {page}',
        reply_markup=markup
    )


@router.callback_query(SupplierItemFilter.filter(F.action == SupplierItemActionEnum.get))
@auth_decorator
async def handle_supplier_item(
        callback_query: types.CallbackQuery,
        callback_data: SupplierItemFilter,
        user: User
):
    supplier: Supplier = await views.get_supplier(bootstrap.uow, callback_data.tg_id)

    if user.is_admin:
        text = f'{supplier.title} ({supplier.alias})'
    else:
        text = supplier.alias

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=html.bold(text),
        reply_markup=kb.get_supplier_item_kb(user, supplier)
    )


router.include_routers(
    create_router,
    update_router,
    delete_router
)
