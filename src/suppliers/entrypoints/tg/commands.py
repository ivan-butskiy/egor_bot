from dataclasses import dataclass


@dataclass(frozen=True)
class SuppliersCommands:
    get_suppliers: str = '🚚 Обрати постачальника'
    create_order: str = '📦 Створити замовлення'

    # compatible to admin
    create_supplier: str = '✅ Додати постачальника'
    edit_supplier: str = '📝 Редагувати'
    delete_supplier: str = '❌ Видалити'
