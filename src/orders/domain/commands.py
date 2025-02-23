from dataclasses import dataclass

from src.app.domain.commands import BaseCommand


@dataclass
class CreateOrderCommand(BaseCommand):
    supplier_tg_id: int
    user_tg_id: int
    message_id: int
    text: str
