from typing import Annotated
from fastapi import Depends

from operations.users import UsersOperation
from dependencies.repositories import UserRepositoryDep

from operations.posts import PostsOperation
from dependencies.repositories import PostRepositoryDep


def get_users_operation(
    user_repository: UserRepositoryDep,
) -> UsersOperation:
    return UsersOperation(user_repository)


UsersOperationDep = Annotated[UsersOperation, Depends(get_users_operation)]


def get_posts_operation(
    post_repository: PostRepositoryDep,
) -> PostsOperation:
    return PostsOperation(post_repository)


PostsOperationDep = Annotated[
    PostsOperation,
    Depends(get_posts_operation),
]
