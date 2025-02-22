import enum

from aiogram.filters.callback_data import CallbackData


class SupplierItemActionEnum(enum.StrEnum):
    get = 'get'
    edit = 'edit'
    remove = 'remove'
    create_order = 'create_order'


class PaginateSuppliersFilter(CallbackData, prefix='paginate_suppliers'):
    page: int


class SupplierItemFilter(CallbackData, prefix='supplier_item'):
    tg_id: int
    action: SupplierItemActionEnum
