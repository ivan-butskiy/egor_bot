import enum

from aiogram.filters.callback_data import CallbackData


class EditUserActionsEnum(enum.StrEnum):
    first_name = 'first_name'
    last_name = 'last_name'
    cancel = 'cancel'


class EditUserFilter(CallbackData, prefix='edit_user'):
    tg_id: int
    action: EditUserActionsEnum
