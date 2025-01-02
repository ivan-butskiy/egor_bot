from aiogram.filters.callback_data import CallbackData


class PaginateSuppliersFilter(CallbackData, prefix='paginate_suppliers'):
    page: int


class SupplierItemFilter(CallbackData, prefix='supplier_item'):
    tg_id: int
