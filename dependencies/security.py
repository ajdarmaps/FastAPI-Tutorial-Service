from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import JWTHandler
from schema.jwt import JWTPayload
from fastapi import HTTPException, status, Depends
from dependencies.repositories import UserRepositoryDep
from typing import Annotated
from db.models import User

security_scheme = HTTPBearer()


async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> JWTPayload:
    return JWTHandler.verify(credentials.credentials)


async def get_current_user(
    user_repository: UserRepositoryDep,
    payload: CurrentToken,
):
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

CurrentToken = Annotated[
    JWTPayload,
    Depends(get_current_token),
]
