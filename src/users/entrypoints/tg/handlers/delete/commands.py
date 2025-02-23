from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteUserCommands:
    approve: str = '✅ Підтвердити видалення'
    reject: str = '❌ Скасувати видалення'
