from dataclasses import dataclass

from src.app.domain.commands import BaseCommand
from src.users.domain.model import UserTypeEnum


@dataclass
class CreateUserCommand(BaseCommand):
    tg_id: int
    first_name: str
    last_name: str
    type: UserTypeEnum


@dataclass
class UpdateUserCommand(BaseCommand):
    tg_id: int
    first_name: str = None
    last_name: str = None


@dataclass
class DeleteUserCommand(BaseCommand):
    tg_id: int

