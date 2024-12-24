from typing import List

from src.domain.suppliers.service.unit_of_work import AbstractUnitOfWork
from src.domain.suppliers import Supplier


async def get_suppliers(
        offset: int,
        limit: int,
        uow: AbstractUnitOfWork
) -> List[Supplier]:
    async with uow:
        return await uow.suppliers.get_list(limit, offset)
