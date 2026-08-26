from uuid import UUID

from db.models import Post

from unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from schema._input import (
    CreatePostInput,
    PaginationInput,
    UpdatePostInput,
)

from core.cache import CacheBackend, get_or_set
from core.cache_keys import build_posts_list_cache_key
from schema.output import PaginatedPostsOutput


from exceptions import (
    PermissionDeniedError,
    PostNotFoundError,
)

import logging

logger = logging.getLogger(__name__)


POSTS_LIST_CACHE_TTL = 60
POSTS_LIST_CACHE_PREFIX = "posts:list:"


class PostsService:

    def __init__(
        self,
        uow: SQLAlchemyUnitOfWork,
        cache: CacheBackend,
    ):
        self.uow = uow
        self.cache = cache

    async def create_post(
        self,
        data: CreatePostInput,
        author_id: UUID,
    ) -> Post:

        async with self.uow:
            post = await self.uow.posts.create(
                data=data,
                author_id=author_id,
            )

            await self.uow.commit()
            logger.info(
                "Post created: post_id=%s author_id=%s",
                post.id,
                author_id,
            )

        await self._invalidate_public_posts_cache()

        return post

    async def get_my_posts(
        self,
        author_id: UUID,
        pagination: PaginationInput,
        search: str | None = None,
    ):
        limit = pagination.page_size
        offset = (pagination.page - 1) * pagination.page_size

        items, total = await self.uow.posts.list_by_author_id(
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

        post = await self.uow.posts.get_by_id(
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

        async with self.uow:
            post = await self._get_owned_post(
                post_id=post_id,
                current_user_id=current_user_id,
            )

            post = await self.uow.posts.update(
                post=post,
                data=data,
            )

            await self.uow.commit()
            logger.info(
                "Post updated: post_id=%s user_id=%s",
                post.id,
                current_user_id,
            )

        await self._invalidate_public_posts_cache()

        return post

    async def delete_post(
        self,
        post_id: UUID,
        current_user_id: UUID,
    ) -> None:

        async with self.uow:
            post = await self._get_owned_post(
                post_id=post_id,
                current_user_id=current_user_id,
            )

            await self.uow.posts.delete(post)

            await self.uow.commit()
            logger.info(
                "Post deleted: post_id=%s user_id=%s",
                post_id,
                current_user_id,
            )

        await self._invalidate_public_posts_cache()

    async def list_public_posts(
        self,
        pagination: PaginationInput,
        search: str | None = None,
        author_id: UUID | None = None,
    ):
        cache_key = build_posts_list_cache_key(
            page=pagination.page,
            page_size=pagination.page_size,
            search=search,
            author_id=author_id,
        )

        async def load_posts() -> dict:
            limit = pagination.page_size
            offset = (pagination.page - 1) * limit

            items, total = await self.uow.posts.list_public(
                search=search,
                author_id=author_id,
                offset=offset,
                limit=limit,
            )

            response = self._build_paginated_response(
                items=items,
                page=pagination.page,
                page_size=limit,
                total=total,
            )

            return PaginatedPostsOutput.model_validate(response).model_dump(mode="json")

        return await get_or_set(
            cache=self.cache,
            key=cache_key,
            factory=load_posts,
            ttl=POSTS_LIST_CACHE_TTL,
        )

    async def _invalidate_public_posts_cache(self) -> None:
        try:
            await self.cache.delete_prefix(POSTS_LIST_CACHE_PREFIX)
        except Exception:
            logger.warning(
                "Cache invalidation failed for prefix=%s",
                POSTS_LIST_CACHE_PREFIX,
                exc_info=True,
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
