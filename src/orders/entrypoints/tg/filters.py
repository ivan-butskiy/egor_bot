import enum

from aiogram.filters.callback_data import CallbackData


class OrderItemActionEnum(enum.StrEnum):
    get = 'get'
    delete = 'delete'


class PaginateOrdersFilter(CallbackData, prefix='paginate_orders'):
    page: int


class OrderItemFilter(CallbackData, prefix='order_item'):
    id: int
    action: OrderItemActionEnum
