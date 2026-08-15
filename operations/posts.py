from uuid import UUID

from db.models import Post
from repositories.post_repository import PostRepository
from schema._input import (
    CreatePostInput,
    PaginationInput,
    UpdatePostInput,
)

from exceptions import (
    PermissionDeniedError,
    PostNotFoundError,
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
        pagination: PaginationInput,
        search: str | None = None,
    ):
        limit = pagination.page_size
        offset = (pagination.page - 1) * pagination.page_size

        items, total = await self.post_repository.list_by_author_id(
            author_id=author_id,
            search=search,
            offset=offset,
            limit=limit,
        )

        total_pages = (total + limit - 1) // limit if total > 0 else 1

        return {
            "items": items,
            "meta": {
                "page": pagination.page,
                "page_size": limit,
                "total": total,
                "total_pages": total_pages,
                "has_next": pagination.page < total_pages,
                "has_previous": pagination.page > 1,
            },
        }

    async def get_post_by_id(
        self,
        post_id: UUID,
    ) -> Post:

        post = await self.post_repository.get_by_id(
            post_id=post_id,
        )

        if post is None:
            raise PostNotFoundError("Post not found")

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

    async def delete_post(
        self,
        post_id: UUID,
        current_user_id: UUID,
    ) -> None:

        post = await self._get_owned_post(
            post_id=post_id,
            current_user_id=current_user_id,
        )

        await self.post_repository.delete(post)

    async def list_public_posts(
        self,
        pagination: PaginationInput,
        search: str | None = None,
        author_id: UUID | None = None,
    ):
        limit = pagination.page_size
        offset = (pagination.page - 1) * limit

        items, total = await self.post_repository.list_public(
            search=search,
            author_id=author_id,
            offset=offset,
            limit=limit,
        )

        return self._build_paginated_response(
            items=items,
            page=pagination.page,
            page_size=limit,
            total=total,
        )

    @staticmethod
    def _build_paginated_response(
        items,
        page: int,
        page_size: int,
        total: int,
    ):
        total_pages = max(
            1,
            (total + page_size - 1) // page_size,
        )

        return {
            "items": items,
            "meta": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
        }