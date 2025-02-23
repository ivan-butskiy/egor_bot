import abc
from typing import Set, List, Any


class BaseAbstractRepository(abc.ABC):

    def __init__(self):
        self.seen: Set[Any] = set()

    async def add(self, entity: Any):
        await self._add(entity)
        self.seen.add(entity)

    async def get(self, id_: int, exclude_id: int = None) -> Any | None:
        user = await self._get(id_, exclude_id)
        if user:
            self.seen.add(user)
        return user

    async def delete(self, id_: int) -> None:
        await self._delete(id_)

    async def get_list(self, limit: int, offset: int) -> List[Any]:
        res = await self._get_list(limit, offset)
        self.seen.union(res)
        return await self._get_list(limit, offset)

    async def count(self) -> int:
        return await self._count()

    async def exists(self) -> bool:
        return await self._exists()

    @abc.abstractmethod
    async def _add(self, entity: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, id_: int, exclude_id: int = None) -> Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self, id_: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_list(self, limit: int, offset: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def _count(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def _exists(self) -> bool:
        raise NotImplementedError
