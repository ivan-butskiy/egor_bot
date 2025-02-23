from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateUserCommands:
    first_name: str = "➖ Ім'я"
    last_name: str = '➖ Прізвище'
    cancel: str = '❌ Скасувати'
