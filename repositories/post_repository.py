from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from uuid import UUID
from db.models import Post
from schema._input import CreatePostInput, UpdatePostInput
from collections.abc import Sequence
from repositories.base_repository import BaseRepository


class PostRepository(BaseRepository):
    def __init__(
        self,
        db_session: AsyncSession,
    ):
        super().__init__(db_session)

    async def create(
        self,
        data: CreatePostInput,
        author_id: UUID,
    ) -> Post:

        post = Post(
            title=data.title,
            content=data.content,
            author_id=author_id,
        )

        try:
            self.db_session.add(post)

            await self.db_session.commit()

            await self.db_session.refresh(post)

            return post

        except Exception:
            await self.db_session.rollback()
            raise

    async def list_by_author_id(
        self,
        author_id: UUID,
    ) -> Sequence[Post]:

        result = await self.db_session.execute(
            sa.select(Post).where(
                Post.author_id == author_id,
            )
        )

        return result.scalars().all()

    async def get_by_id(
        self,
        post_id: UUID,
    ) -> Post | None:

        result = await self.db_session.execute(
            sa.select(Post).where(
                Post.id == post_id,
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        post: Post,
        data: UpdatePostInput,
    ) -> Post:

        if data.title is not None:
            post.title = data.title

        if data.content is not None:
            post.content = data.content

        await self.db_session.commit()
        await self.db_session.refresh(post)

        return post

    async def delete(
        self,
        post: Post,
    ) -> None:
        await self.db_session.delete(post)
        await self.db_session.commit()
