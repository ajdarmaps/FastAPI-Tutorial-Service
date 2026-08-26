from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import JWTHandler
from db.models import User, UserRole
from dependencies.unit_of_work import UnitOfWorkDep
from schema.jwt import JWTPayload
from exceptions import PermissionDeniedError

security_scheme = HTTPBearer()


async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> JWTPayload:
    return JWTHandler.verify(credentials.credentials)


CurrentToken = Annotated[
    JWTPayload,
    Depends(get_current_token),
]


async def get_current_user(
    uow: UnitOfWorkDep,
    payload: CurrentToken,
) -> User:
    user = await uow.users.get_by_id(payload.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def require_admin(
    current_user: CurrentUser,
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise PermissionDeniedError(
            "Admin permission required."
        )

    return current_user

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]

AdminUser = Annotated[
    User,
    Depends(require_admin),
]
