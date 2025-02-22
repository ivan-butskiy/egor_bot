from aiogram import Router, F
from aiogram import types
from aiogram.utils import markdown

from src.app.entrypoints.tg.utils import auth_decorator
from src.app.entrypoints.tg.handlers import keyboards as base_kbs
from src.users import User
from src.suppliers.domain.commands import DeleteSupplier
from src.suppliers.bootstrap import bootstrap
from src.suppliers.entrypoints.tg.filters import SupplierItemFilter, SupplierItemActionEnum
from .keyboards import get_delete_supplier_keyboard
from .filters import DeleteSupplierFilter, DeleteSupplierActionsEnum


router = Router(name=__name__)


@router.callback_query(SupplierItemFilter.filter(F.action == SupplierItemActionEnum.delete))
async def handle_delete_supplier(
        callback_query: types.CallbackQuery,
        callback_data: SupplierItemFilter,
) -> None:
    text = markdown.text(
        markdown.hbold('Підтвердіть дію.\n'),
        markdown.text('Ви впевнені, що бажаєте видалити постачальника? '
                      'Разом з ним будуть видалені пов\'язані замовлення. '
                      'Після видалення скасувати цю дію буде неможливо'),
        sep='\n'
    )

    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=get_delete_supplier_keyboard(callback_data.tg_id)
    )

@router.callback_query(DeleteSupplierFilter.filter(F.action == DeleteSupplierActionsEnum.approve))
@auth_decorator
async def handle_approve_delete(
        callback_query: types.CallbackQuery,
        callback_data: DeleteSupplierFilter,
        user: User
):
    cmd = DeleteSupplier(tg_id=callback_data.tg_id)
    await bootstrap.handle(cmd)
    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Постачальника успішно видалено.',
        reply_markup=base_kbs.get_start_kb(user)
    )


@router.callback_query(DeleteSupplierFilter.filter(F.action == DeleteSupplierActionsEnum.reject))
@auth_decorator
async def handle_reject_delete(callback_query: types.CallbackQuery, user: User):
    await callback_query.answer()
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Видалення скасовано.',
        reply_markup=base_kbs.get_start_kb(user)
    )
