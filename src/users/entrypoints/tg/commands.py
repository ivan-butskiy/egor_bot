from dataclasses import dataclass


@dataclass(frozen=True)
class UsersCommand:
    get_users: str = '🫡 Обрати користувача'
    create_user: str = '✅ Додати користувача'
    edit_user: str = '📝 Редагувати'
    delete_user: str = '❌ Видалити'
