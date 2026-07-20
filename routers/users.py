from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.engine import get_db
from operations.users import UsersOperation
from schema._input import (
    RegisterInput,
    UpdateUserProfileInput,
    DeleteUserAccountInput,
)
from repositories.user_repository import UserRepository

router = APIRouter()


@router.post("/register")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: RegisterInput = Body(),
):
    user_repository = UserRepository(db_session)
    user = await UsersOperation(user_repository).create(
        username=data.username,
        password=data.password,
    )
    return user


@router.post("/login")
async def login(): ...


@router.get("/{username}")
async def get_user_profile(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    username: str,
):
    user_repository = UserRepository(db_session)
    user_profile = await UsersOperation(user_repository).get_user_by_username(username)

    return user_profile


@router.put("/")
async def update_user_profile(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UpdateUserProfileInput = Body(),
):
    user_repository = UserRepository(db_session)
    user_profile = await UsersOperation(user_repository).update_user_profile(
        old_username=data.old_username,
        new_username=data.new_username,
    )

    return user_profile


@router.delete("/", status_code=204)
async def delete_user_account(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: DeleteUserAccountInput = Body(),
):
    user_repository = UserRepository(db_session)
    await UsersOperation(user_repository).delete_user_account(
        username=data.username,
        password=data.password,
    )
