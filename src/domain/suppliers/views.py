from typing import List

from src.domain.suppliers.service.unit_of_work import AbstractUnitOfWork
from src.domain.suppliers import Supplier


async def get_suppliers(
        offset: int,
        limit: int,
        uow: AbstractUnitOfWork
) -> List[Supplier]:
    async with uow:
        items = await uow.suppliers.get_list(limit, offset)
        return items


async def get_suppliers_count(uow: AbstractUnitOfWork) -> int:
    async with uow:
        return await uow.suppliers.count()
