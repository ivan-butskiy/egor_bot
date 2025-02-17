from typing import Tuple, List

from src.suppliers.service.unit_of_work import AbstractUnitOfWork
from src.suppliers import Supplier


async def get_suppliers(
        uow: AbstractUnitOfWork,
        offset: int = 0,
        limit: int = 10,
) -> Tuple[List[Supplier], int]:
    async with uow:
        items = await uow.suppliers.get_list(limit, offset)
        count = await uow.suppliers.count()
        return items, count


async def get_supplier(uow: AbstractUnitOfWork, tg_id: int) -> Supplier:
    async with uow:
        return await uow.suppliers.get(tg_id)


async def get_suppliers_count(uow: AbstractUnitOfWork) -> int:
    async with uow:
        return await uow.suppliers.count()


async def exists_suppliers(uow: AbstractUnitOfWork) -> bool:
    async with uow:
        return await uow.suppliers.exists()


async def check_supplier_title(uow: AbstractUnitOfWork, title: str) -> bool:
    async with uow:
        return not await uow.suppliers.exists_by_title(title)


async def check_supplier_alias(uow: AbstractUnitOfWork, alias: str) -> bool:
    async with uow:
        return not await uow.suppliers.exists_by_alias(alias)
