from uuid import UUID

from repositories.post_repository import PostRepository
from schema._input import CreatePostInput, UpdatePostInput
from db.models import Post
from collections.abc import Sequence

from exceptions import (
    PostNotFoundError,
    PermissionDeniedError,
)


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

    async def get_my_posts(
        self,
        author_id: UUID,
    ) -> Sequence[Post]:

        return await self.post_repository.list_by_author_id(
            author_id=author_id,
        )

    async def get_post_by_id(
        self,
        post_id: UUID,
    ) -> Post:

        post = await self.post_repository.get_by_id(
            post_id=post_id,
        )

        if post is None:
            raise PostNotFoundError(
                "Post not found",
            )

        return post

    async def _get_owned_post(
        self,
        post_id: UUID,
        current_user_id: UUID,
    ) -> Post:

        post = await self.get_post_by_id(
            post_id=post_id,
        )

        if post.author_id != current_user_id:
            raise PermissionDeniedError(
                "You don't have permission to access this post."
            )

        return post

    async def update_post(
        self,
        post_id: UUID,
        data: UpdatePostInput,
        current_user_id: UUID,
    ) -> Post:

        post = await self._get_owned_post(
            post_id=post_id,
            current_user_id=current_user_id,
        )

        return await self.post_repository.update(
            post=post,
            data=data,
        )
