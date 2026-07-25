from typing import Annotated
from fastapi import Depends

from repositories.user_repository import UserRepository
from dependencies.database import DbSession


def get_user_repository(
    db_session: DbSession,
) -> UserRepository:
    return UserRepository(db_session)


UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository)
]