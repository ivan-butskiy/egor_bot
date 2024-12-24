import enum
from dataclasses import dataclass


class MessengerTypeEnum(enum.StrEnum):
    telegram = 'telegram'
    viber = 'viber'
    whatsapp = 'whatsapp'


@dataclass
class Supplier:
    id: int
    title: str
    alias: str
    messenger: MessengerTypeEnum
    phone_number: str

    def __hash__(self) -> int:
        return hash(self.id)
