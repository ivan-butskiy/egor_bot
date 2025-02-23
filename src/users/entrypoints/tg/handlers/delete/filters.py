import enum

from aiogram.filters.callback_data import CallbackData


class DeleteUserActionsEnum(enum.StrEnum):
    approve = 'approve'
    reject = 'reject'


class DeleteUserFilter(CallbackData, prefix='delete_user'):
    tg_id: int
    action: DeleteUserActionsEnum
