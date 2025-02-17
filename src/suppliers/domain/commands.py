from dataclasses import dataclass
from src.app.domain.commands import BaseCommand


@dataclass
class CreateSupplier(BaseCommand):
    tg_id: int
    title: str
    alias: str
