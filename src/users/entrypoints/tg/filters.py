import enum

from aiogram.filters.callback_data import CallbackData


class UserItemActionEnum(enum.StrEnum):
    get = 'get'
    edit = 'edit'
    delete = 'delete'


class PaginateUsersFilter(CallbackData, prefix='paginate_users'):
    page: int


class UserItemFilter(CallbackData, prefix='user_item'):
    tg_id: int
    action: UserItemActionEnum
