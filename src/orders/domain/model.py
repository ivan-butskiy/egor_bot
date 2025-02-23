from datetime import datetime
from dataclasses import dataclass, field

import pytz

from src.app.utils import get_utc_now
from src.suppliers import Supplier
from src.users import User


@dataclass
class Order:
    supplier_tg_id: int
    user_tg_id: int
    message_id: int
    text: str
    created_at: datetime = field(default_factory=get_utc_now)

    # primary key
    id: int = field(default=None, init=False)

    # related objects
    supplier: Supplier = field(default=None, init=False)
    user: User = field(default=None, init=False)

    def created_at_as_tz(self, tz: pytz.BaseTzInfo = pytz.timezone('Europe/Kyiv')):
        return self.created_at.astimezone(tz).replace(tzinfo=None)

    def __repr__(self) -> str:
        return f'<Order (id={self.id}, supplier_tg_id={self.supplier_tg_id}, user_tg_id={self.user_tg_id})>'

    def __hash__(self) -> int:
        return hash(self.id)
