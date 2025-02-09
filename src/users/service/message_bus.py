from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import unit_of_work


class MessageBus:

    def __init__(
            self,
            uow: 'unit_of_work.AbstractUnitOfWork'
    ):
        self.uow = uow
