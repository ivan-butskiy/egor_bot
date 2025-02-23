from dataclasses import dataclass

from src.app.domain.commands import BaseCommand


@dataclass
class CreateSupplierCommand(BaseCommand):
    tg_id: int
    title: str
    alias: str


@dataclass
class UpdateSupplierCommand(BaseCommand):
    tg_id: int
    new_tg_id: int = None
    title: str = None
    alias: str = None


@dataclass
class DeleteSupplierCommand(BaseCommand):
    tg_id: int
