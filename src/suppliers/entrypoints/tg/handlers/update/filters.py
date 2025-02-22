import enum

from aiogram.filters.callback_data import CallbackData


class EditSupplierActionsEnum(enum.StrEnum):
    contact = 'contact'
    title = 'title'
    alias = 'alias'
    cancel = 'cancel'


class EditSupplierFilter(CallbackData, prefix='edit_supplier'):
    tg_id: int
    action: EditSupplierActionsEnum
