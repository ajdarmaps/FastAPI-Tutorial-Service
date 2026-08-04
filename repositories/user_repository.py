from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from uuid import UUID
from core.hashing import password_manager
from db.models import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(
        self,
        db_session: AsyncSession,
    ):
        super().__init__(db_session)

    async def create(
        self,
        username: str,
        password: str,
    ) -> User | None:
        user = await self.get_by_username(username)
        if user is None:
            new_user = User(username=username, password=password)
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)

            return new_user
        return None

    async def get_by_username(self, username: str) -> User | None:

        query = sa.select(User).where(User.username == username)

        result = await self.db_session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        result = await self.db_session.execute(
            sa.select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_by_username(
        self,
        old_username: str,
        new_username: str,
    ) -> User | None:

        result = await self.db_session.execute(
            sa.select(User).where(User.username == old_username)
        )

        user = result.scalar_one_or_none()

        if user is None:
            return None

        user.username = new_username

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user


async def delete(
    self,
    user_id: UUID,
    password: str,
) -> User | None:

    result = await self.db_session.execute(sa.select(User).where(User.id == user_id))

    user = result.scalar_one_or_none()

    if user is None:
        return None

    if not password_manager.verify(
        password,
        user.password,
    ):
        return None

    await self.db_session.delete(user)
    await self.db_session.commit()

    return user
