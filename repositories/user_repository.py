from uuid import UUID

import sqlalchemy as sa

from db.models import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    async def create(
        self,
        username: str,
        password: str,
    ) -> User | None:

        user = await self.get_by_username(username)

        if user is not None:
            return None

        new_user = User(
            username=username,
            password=password,
        )

        self.db_session.add(new_user)

        await self.db_session.flush()
        await self.db_session.refresh(new_user)

        return new_user

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:

        result = await self.db_session.execute(
            sa.select(User).where(
                User.username == username,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        result = await self.db_session.execute(
            sa.select(User).where(
                User.id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def update_by_username(
        self,
        old_username: str,
        new_username: str,
    ) -> User | None:

        result = await self.db_session.execute(
            sa.select(User).where(
                User.username == old_username,
            )
        )

        user = result.scalar_one_or_none()

        if user is None:
            return None

        user.username = new_username

        await self.db_session.flush()
        await self.db_session.refresh(user)

        return user

    async def delete(
        self,
        user: User,
    ) -> None:

        await self.db_session.delete(user)
        await self.db_session.flush()

    async def list_users(self) -> list[User]:
        result = await self.db_session.execute(
            sa.select(User).order_by(User.username)
        )

        return list(result.scalars().all())
