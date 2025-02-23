from dataclasses import dataclass


@dataclass
class Supplier:
    tg_id: int
    title: str
    alias: str

    def __repr__(self) -> str:
        return f'<Supplier (tg_id={self.tg_id}, title={self.title}, alias={self.alias})>'

    def __hash__(self) -> int:
        return hash(self.tg_id)
