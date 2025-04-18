import enum
from dataclasses import dataclass, field


class UserTypeEnum(enum.StrEnum):
    admin = 'admin'
    manager = 'manager'


@dataclass
class User:
    tg_id: int
    first_name: str
    last_name: str = field(default=None)
    type: UserTypeEnum = field(default=UserTypeEnum.manager)

    @property
    def is_admin(self) -> bool:
        return self.type == UserTypeEnum.admin

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    @property
    def button_repr(self):
        if self.is_admin:
            return f'⭐ {self.full_name}'
        return self.full_name

    def __hash__(self) -> int:
        return hash(self.tg_id)
