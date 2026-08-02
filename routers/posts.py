from fastapi import APIRouter
from schema._input import CreatePostInput
from schema.output import PostOutput

from dependencies.operations import PostsOperationDep
from dependencies.security import CurrentUser

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
