from typing import Annotated
from fastapi import Depends

from repositories.user_repository import UserRepository
from dependencies.database import DbSession
from repositories.post_repository import PostRepository


def get_user_repository(
    db_session: DbSession,
) -> UserRepository:
    return UserRepository(db_session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_post_repository(
    db_session: DbSession,
) -> PostRepository:
    return PostRepository(db_session)


PostRepositoryDep = Annotated[
    PostRepository,
    Depends(get_post_repository),
]
