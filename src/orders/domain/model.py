from datetime import datetime
from dataclasses import dataclass, field

import pytz

from src.app.utils import get_utc_now
from src.suppliers import Supplier
from src.users import User


@dataclass
class Order:
    id: int
    supplier_tg_id: int
    user_tg_id: int
    message_id: int
    text: str
    created_at: datetime = field(default_factory=get_utc_now)

    # related objects
    supplier: Supplier = None
    user: User = None

    def created_at_as_tz(self, tz: pytz.BaseTzInfo = pytz.timezone('Europe/Kyiv')):
        return self.created_at.astimezone(tz).replace(tzinfo=None)

    def __repr__(self) -> str:
        return f'<Order (id={self.id})>'

    def __hash__(self) -> int:
        return hash(self.id)
