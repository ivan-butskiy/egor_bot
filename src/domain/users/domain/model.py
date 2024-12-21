import enum
from dataclasses import dataclass


class UserTypeEnum(enum.StrEnum):
    admin = 'admin'
    manager = 'manager'


@dataclass
class User:
    tg_id: int
    user_name: str
    first_name: str
    last_name: str
    type: UserTypeEnum

    @property
    def is_admin(self) -> bool:
        return self.type == UserTypeEnum.admin

    # def __repr__(self) -> str:
    #     return f'<User (tg_id={self.tg_id}, user_name={self.user_name}, first_name={self.first_name}, last_name={self.last_name} type={self.type})>'
