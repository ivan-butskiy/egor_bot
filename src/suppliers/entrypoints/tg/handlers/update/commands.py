from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateSupplierCommands:
    contact: str = '📱 Контакт'
    title: str = '🤫 Назву'
    alias: str = '😎 Псевдонім'
    cancel: str = '❌ Скасувати'
