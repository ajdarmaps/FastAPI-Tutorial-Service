from uuid import UUID

from fastapi import APIRouter, status

from dependencies.operations import PostsServiceDep
from dependencies.pagination import PaginationDep
from dependencies.security import CurrentUser
from schema._input import CreatePostInput, UpdatePostInput
from schema.output import PaginatedPostsOutput, PostOutput

router = APIRouter()


@router.post(
    "/",
    response_model=PostOutput,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    data: CreatePostInput,
    operation: PostsServiceDep,
    current_user: CurrentUser,
) -> PostOutput:
    return await operation.create_post(
        data=data,
        author_id=current_user.id,
    )


@router.get(
    "/my-posts",
    response_model=PaginatedPostsOutput,
)
async def get_my_posts(
    operation: PostsServiceDep,
    current_user: CurrentUser,
    pagination: PaginationDep,
    search: str | None = None,
) -> PaginatedPostsOutput:
    return await operation.get_my_posts(
        author_id=current_user.id,
        pagination=pagination,
        search=search,
    )


@router.get(
    "/{post_id}",
    response_model=PostOutput,
)
async def get_post(
    post_id: UUID,
    operation: PostsServiceDep,
) -> PostOutput:
    return await operation.get_post_by_id(
        post_id=post_id,
    )


@router.patch(
    "/{post_id}",
    response_model=PostOutput,
)
async def update_post(
    post_id: UUID,
    data: UpdatePostInput,
    operation: PostsServiceDep,
    current_user: CurrentUser,
) -> PostOutput:
    return await operation.update_post(
        post_id=post_id,
        data=data,
        current_user_id=current_user.id,
    )


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    post_id: UUID,
    operation: PostsServiceDep,
    current_user: CurrentUser,
) -> None:
    await operation.delete_post(
        post_id=post_id,
        current_user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=PaginatedPostsOutput,
)
async def list_public_posts(
    operation: PostsServiceDep,
    pagination: PaginationDep,
    search: str | None = None,
    author_id: UUID | None = None,
) -> PaginatedPostsOutput:
    return await operation.list_public_posts(
        pagination=pagination,
        search=search,
        author_id=author_id,
    )
