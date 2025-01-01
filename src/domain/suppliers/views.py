from typing import Tuple, List

from src.domain.suppliers.service.unit_of_work import AbstractUnitOfWork
from src.domain.suppliers import Supplier


async def get_suppliers(
        uow: AbstractUnitOfWork,
        offset: int,
        limit: int = 10,
) -> Tuple[List[Supplier], int]:
    async with uow:
        items = await uow.suppliers.get_list(limit, offset)
        count = await uow.suppliers.count()
        return items, count


async def get_supplier(uow: AbstractUnitOfWork, item_id: int) -> Supplier:
    async with uow:
        return await uow.suppliers.get(item_id)


async def get_suppliers_count(uow: AbstractUnitOfWork) -> int:
    async with uow:
        return await uow.suppliers.count()
