from typing import Annotated

from fastapi import Depends

from dependencies.unit_of_work import UnitOfWorkDep

from services.users import UsersOperation
from services.posts import PostsService

from dependencies.cache import CacheDep


def get_users_operation(
    uow: UnitOfWorkDep,
) -> UsersOperation:
    return UsersOperation(uow)


UsersOperationDep = Annotated[
    UsersOperation,
    Depends(get_users_operation),
]


def get_posts_service(
    uow: UnitOfWorkDep,
    cache: CacheDep,
) -> PostsService:
    return PostsService(
        uow=uow,
        cache=cache,
    )


PostsServiceDep = Annotated[
    PostsService,
    Depends(get_posts_service),
]
