from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteSupplierCommands:
    approve: str = '✅ Підтвердити видалення'
    reject: str = '❌ Скасувати видалення'
