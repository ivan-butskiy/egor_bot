from dataclasses import dataclass

from src.app.domain.commands import BaseCommand
from src.users.domain.model import UserTypeEnum


@dataclass
class CreateUserCommand(BaseCommand):
    tg_id: int
    first_name: str
    last_name: str
    type: UserTypeEnum
