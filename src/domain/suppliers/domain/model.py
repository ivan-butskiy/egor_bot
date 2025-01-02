from dataclasses import dataclass


@dataclass
class Supplier:
    tg_id: int
    title: str
    alias: str

    def __hash__(self) -> int:
        return hash(self.tg_id)
