import enum
from dataclasses import dataclass


class MessengerTypeEnum(enum.StrEnum):
    telegram = 'telegram'
    whatsapp = 'whatsapp'


@dataclass
class Supplier:
    id: int
    title: str
    alias: str
    messenger: MessengerTypeEnum
    phone: str

    def __hash__(self) -> int:
        return hash(self.id)
