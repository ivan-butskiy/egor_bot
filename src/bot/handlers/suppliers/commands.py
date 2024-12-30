from dataclasses import dataclass


@dataclass(frozen=True)
class SuppliersCommands:
    get_suppliers: str = 'Обрати постачальника 👉'
    add_supplier: str = 'Додати постачальника ✅'
