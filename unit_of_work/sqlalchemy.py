from sqlalchemy.ext.asyncio import AsyncSession

from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository

from unit_of_work.base import AbstractUnitOfWork


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session: AsyncSession):
        self.session = session

        self.posts = PostRepository(session)
        self.users = UserRepository(session)

    async def __aenter__(self):
        return self

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()