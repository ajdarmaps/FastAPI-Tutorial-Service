from typing import Annotated
from fastapi import Depends

from operations.users import UsersOperation
from dependencies.repositories import UserRepositoryDep


def get_users_operation(
    user_repository: UserRepositoryDep,
) -> UsersOperation:
    return UsersOperation(user_repository)


UsersOperationDep = Annotated[
    UsersOperation,
    Depends(get_users_operation)
]