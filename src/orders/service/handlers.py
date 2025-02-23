from src.orders.service.unit_of_work import AbstractUnitOfWork
from src.orders.domain import commands
from src.orders import Order


async def create_order(cmd: commands.CreateOrderCommand, uow: AbstractUnitOfWork):
    async with uow:
        instance = Order(
            supplier_tg_id=cmd.supplier_tg_id,
            user_tg_id=cmd.user_tg_id,
            message_id=cmd.message_id,
            text=cmd.text
        )

        await uow.orders.add(instance)
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateOrderCommand: create_order
}

EVENT_HANDLERS = {}
