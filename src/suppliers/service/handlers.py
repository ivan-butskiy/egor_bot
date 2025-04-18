from src.suppliers.service.unit_of_work import AbstractUnitOfWork
from src.suppliers.domain import commands
from src.suppliers import Supplier


async def create_supplier(cmd: commands.CreateSupplierCommand, uow: AbstractUnitOfWork):
    async with uow:
        instance = Supplier(
            tg_id=cmd.tg_id,
            title=cmd.title,
            alias=cmd.alias
        )

        await uow.suppliers.add(instance)
        await uow.commit()


async def update_supplier(cmd: commands.UpdateSupplierCommand, uow: AbstractUnitOfWork):
    async with uow:
        instance: Supplier = await uow.suppliers.get(cmd.tg_id)

        if cmd.new_tg_id:
            instance.tg_id = cmd.new_tg_id
        if cmd.title:
            instance.title = cmd.title
        if cmd.alias:
            instance.alias = cmd.alias
        await uow.commit()


async def delete_supplier(cmd: commands.DeleteSupplierCommand, uow: AbstractUnitOfWork):
    async with uow:
        await uow.suppliers.delete(cmd.tg_id)
        await uow.commit()


COMMAND_HANDLERS = {
    commands.CreateSupplierCommand: create_supplier,
    commands.UpdateSupplierCommand: update_supplier,
    commands.DeleteSupplierCommand: delete_supplier
}

EVENT_HANDLERS = {}
