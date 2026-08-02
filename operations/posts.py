from uuid import UUID

from repositories.post_repository import PostRepository
from schema._input import CreatePostInput
from db.models import Post


class PostsOperation:

    def __init__(
        self,
        post_repository: PostRepository,
    ):
        self.post_repository = post_repository

    async def create_post(
        self,
        data: CreatePostInput,
        author_id: UUID,
    ) -> Post:

        return await self.post_repository.create(
            data=data,
            author_id=author_id,
        )
