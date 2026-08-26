from collections.abc import Sequence
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, raiseload


from db.models import Post, User
from repositories.base_repository import BaseRepository
from schema._input import CreatePostInput, UpdatePostInput


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

        self.db_session.add(post)

        await self.db_session.flush()
        await self.db_session.refresh(post)

        return post

    async def _list(
        self,
        filters: list,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Post], int]:

        query = (
            sa.select(Post)
            .options(
                joinedload(Post.author).load_only(
                    User.id,
                    User.username,
                    raiseload=True,
                ),
                raiseload("*"),
            )
            .where(*filters)
            .order_by(
                Post.created_at.desc(),
                Post.id.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        items_result = await self.db_session.execute(query)

        count_query = sa.select(func.count()).select_from(Post).where(*filters)

        total_result = await self.db_session.execute(count_query)

        return (
            items_result.scalars().all(),
            total_result.scalar_one(),
        )

    async def list_by_author_id(
        self,
        author_id: UUID,
        search: str | None,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Post], int]:

        filters = [
            Post.author_id == author_id,
        ]

        if search:
            pattern = f"%{search}%"

            filters.append(
                or_(
                    Post.title.ilike(pattern),
                    Post.content.ilike(pattern),
                )
            )

        return await self._list(
            filters=filters,
            offset=offset,
            limit=limit,
        )

    async def list_public(
        self,
        search: str | None,
        author_id: UUID | None,
        offset: int,
        limit: int,
    ) -> tuple[Sequence[Post], int]:

        filters = []

        if search:
            pattern = f"%{search}%"

            filters.append(
                or_(
                    Post.title.ilike(pattern),
                    Post.content.ilike(pattern),
                )
            )

        if author_id is not None:
            filters.append(
                Post.author_id == author_id,
            )

        return await self._list(
            filters=filters,
            offset=offset,
            limit=limit,
        )

    async def get_by_id(
        self,
        post_id: UUID,
    ) -> Post | None:

        result = await self.db_session.execute(
            sa.select(Post)
            .options(
                joinedload(Post.author).load_only(
                    User.id,
                    User.username,
                    raiseload=True,
                ),
                raiseload("*"),
            )
            .where(
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

        await self.db_session.flush()
        await self.db_session.refresh(post)

        return post

    async def delete(
        self,
        post: Post,
    ) -> None:

        await self.db_session.delete(post)
        await self.db_session.flush()
