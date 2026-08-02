from fastapi import APIRouter, Body
from schema._input import (
    UserInput,
    UpdateUserProfileInput,
    DeleteUserAccountInput,
)
from schema.output import UserOutput
from dependencies.operations import UsersOperationDep
from dependencies.security import CurrentUser

router = APIRouter()


@router.post(
    "/register",
    response_model=UserOutput,
)
async def register(
    operation: UsersOperationDep,
    data: UserInput = Body(),
):
    return await operation.create(
        username=data.username,
        password=data.password,
    )


@router.post("/login")
async def login(
    operation: UsersOperationDep,
    data: UserInput = Body(),
):
    return await operation.login(
        username=data.username,
        password=data.password,
    )


@router.put("/profile")
async def update_user_profile(
    operation: UsersOperationDep,
    data: UpdateUserProfileInput,
):
    return await operation.update_user_profile(
        old_username=data.old_username,
        new_username=data.new_username,
    )


@router.delete("/", status_code=204)
async def delete_user_account(
    operation: UsersOperationDep,
    current_user: CurrentUser,
    data: DeleteUserAccountInput,
):
    await operation.delete_user_account(
        user_id=current_user.id,
        password=data.password,
    )


@router.get(
    "/me",
    response_model=UserOutput,
)
async def me(
    current_user: CurrentUser,
):
    return current_user


@router.get("/{username}", response_model=UserOutput)
async def get_user_profile(
    operation: UsersOperationDep,
    username: str,
):
    return await operation.get_user_by_username(
        username=username,
    )
