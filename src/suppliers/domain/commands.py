from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateSupplier(Command):
    tg_id: int
    title: str
    alias: str
