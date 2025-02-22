from dataclasses import dataclass
from src.app.domain.commands import BaseCommand


@dataclass
class CreateSupplier(BaseCommand):
    tg_id: int
    title: str
    alias: str


@dataclass
class UpdateSupplier(BaseCommand):
    tg_id: int
    new_tg_id: int = None
    title: str = None
    alias: str = None


@dataclass
class DeleteSupplier(BaseCommand):
    tg_id: int
