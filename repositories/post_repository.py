from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db.models import Post
from schema._input import CreatePostInput


class PostRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

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
