import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.domain import User


class AbstractUserRepository:
    pass


class UsersSqlAlchemyRepository(AbstractUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _add(self, user: User):
        self.session.add(user)

    async def _get(self, tg_id: int) -> User | None:
        res = await (
            self.session.execute(
                sa.select(User)
                .where(User.tg_id == tg_id))
        )
        return res.scalar()
