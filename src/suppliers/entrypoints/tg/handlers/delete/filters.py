import enum

from aiogram.filters.callback_data import CallbackData


class DeleteSupplierActionsEnum(enum.StrEnum):
    approve = 'approve'
    reject = 'reject'


class DeleteSupplierFilter(CallbackData, prefix='edit_supplier'):
    tg_id: int
    action: DeleteSupplierActionsEnum
