from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from db.models import User


class UserRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, username: str, password: str) -> User:

        user = User(username=username, password=password)

        self.db_session.add(user)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def get_by_username(self, username: str) -> User | None:

        query = sa.select(User).where(User.username == username)

        result = await self.db_session.execute(query)

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

    async def delete_user(
        self,
        username: str,
        password: str,
    ) -> User | None:

        result = await self.db_session.execute(
            sa.select(User).where(
                User.username == username,
                User.password == password,
            )
        )

        user = result.scalar_one_or_none()

        if user is None:
            return None

        await self.db_session.delete(user)
        await self.db_session.commit()

        return user
