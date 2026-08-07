from fastapi import APIRouter
from schema._input import CreatePostInput, UpdatePostInput
from schema.output import PostOutput

from dependencies.operations import PostsOperationDep
from dependencies.security import CurrentUser
from dependencies.pagination import PaginationDep

from uuid import UUID

router = APIRouter()


@router.post(
    "/",
    response_model=PostOutput,
    status_code=201,
)
async def create_post(
    data: CreatePostInput,
    operation: PostsOperationDep,
    current_user: CurrentUser,
):
    return await operation.create_post(
        data=data,
        author_id=current_user.id,
    )


@router.get(
    "/my-posts",
    response_model=list[PostOutput],
)
async def get_my_posts(
    operation: PostsOperationDep,
    current_user: CurrentUser,
    pagination: PaginationDep,
):
    return await operation.get_my_posts(
        author_id=current_user.id,
        pagination=pagination,
    )


@router.get(
    "/{post_id}",
    response_model=PostOutput,
)
async def get_post(
    post_id: UUID,
    operation: PostsOperationDep,
):
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
    operation: PostsOperationDep,
    current_user: CurrentUser,
):
    return await operation.update_post(
        post_id=post_id,
        data=data,
        current_user_id=current_user.id,
    )

@router.delete(
    "/{post_id}",
    status_code=204,
)
async def delete_post(
    post_id: UUID,
    operation: PostsOperationDep,
    current_user: CurrentUser,
):
    await operation.delete_post(
        post_id=post_id,
        current_user_id=current_user.id,
    )
