from src.suppliers.service.unit_of_work import AbstractUnitOfWork
from src.suppliers.domain import commands
from src.suppliers import Supplier


async def create_supplier(cmd: commands.CreateSupplier, uow: AbstractUnitOfWork):
    async with uow:
        instance = Supplier(
            tg_id=cmd.tg_id,
            title=cmd.title,
            alias=cmd.alias
        )

        await uow.suppliers.add(instance)
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateSupplier: create_supplier
}

EVENT_HANDLERS = {}
