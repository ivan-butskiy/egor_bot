import enum
from dataclasses import dataclass, field


class UserTypeEnum(enum.StrEnum):
    admin = 'admin'
    manager = 'manager'


@dataclass
class User:
    tg_id: int
    user_name: str
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

    def __hash__(self) -> int:
        return hash(self.tg_id)

    # def __repr__(self) -> str:
    #     return f'<User (tg_id={self.tg_id}, user_name={self.user_name}, first_name={self.first_name}, last_name={self.last_name} type={self.type})>'
