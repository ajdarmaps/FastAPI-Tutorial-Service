from fastapi import APIRouter, status, BackgroundTasks
from services.notifications import send_welcome_notification

from dependencies.operations import UsersOperationDep
from dependencies.security import CurrentUser, AdminUser
from schema._input import (
    DeleteUserAccountInput,
    UpdateUserProfileInput,
    UserInput,
)
from schema.jwt import JWTResponsePayload
from schema.output import UserOutput

router = APIRouter()


@router.post(
    "/register",
    response_model=UserOutput,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    operation: UsersOperationDep,
    data: UserInput,
    background_tasks: BackgroundTasks,
) -> UserOutput:
    user = await operation.create(
        username=data.username,
        password=data.password,
    )

    background_tasks.add_task(
        send_welcome_notification,
        user.username,
    )

    return UserOutput.model_validate(user)


@router.post(
    "/login",
    response_model=JWTResponsePayload,
)
async def login(
    operation: UsersOperationDep,
    data: UserInput,
) -> JWTResponsePayload:
    return await operation.login(
        username=data.username,
        password=data.password,
    )


@router.patch(
    "/profile",
    response_model=UserOutput,
)
async def update_user_profile(
    operation: UsersOperationDep,
    current_user: CurrentUser,
    data: UpdateUserProfileInput,
) -> UserOutput:
    return await operation.update_user_profile(
        old_username=current_user.username,
        new_username=data.new_username,
    )


@router.delete(
    "/account",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_account(
    operation: UsersOperationDep,
    current_user: CurrentUser,
    data: DeleteUserAccountInput,
) -> None:
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
) -> UserOutput:
    return current_user


@router.get(
    "/",
    response_model=list[UserOutput],
)
async def list_users(
    operation: UsersOperationDep,
    current_user: AdminUser,
) -> list[UserOutput]:
    return await operation.get_all_users()


@router.get(
    "/{username}",
    response_model=UserOutput,
)
async def get_user_profile(
    operation: UsersOperationDep,
    username: str,
) -> UserOutput:
    return await operation.get_user_by_username(
        username=username,
    )
