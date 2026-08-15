from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import JWTHandler
from db.models import User
from dependencies.repositories import UserRepositoryDep
from schema.jwt import JWTPayload


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
    user_repository: UserRepositoryDep,
    payload: CurrentToken,
) -> User:
    user = await user_repository.get_by_id(payload.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]