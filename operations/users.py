from uuid import UUID

from core.hashing import password_manager
from core.security import JWTHandler
from db.models import User
from exceptions import (
    InvalidUsernamePassword,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from repositories.user_repository import UserRepository
from schema.jwt import JWTResponsePayload


class UsersOperation:

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def create(
        self,
        username: str,
        password: str,
    ) -> User:

        hashed_password = password_manager.hash(password)

        user = await self.user_repository.create(
            username=username,
            password=hashed_password,
        )

        if user is None:
            raise UserAlreadyExistsError(
                "Username already exists"
            )

        return user

    async def get_user_by_username(
        self,
        username: str,
    ) -> User:

        user = await self.user_repository.get_by_username(
            username
        )

        if user is None:
            raise UserNotFoundError(
                "User not found"
            )

        return user

    async def update_user_profile(
        self,
        old_username: str,
        new_username: str,
    ) -> User:

        user = await self.get_user_by_username(
            old_username
        )

        existing_user = await self.user_repository.get_by_username(
            new_username
        )

        if (
            existing_user is not None
            and existing_user.id != user.id
        ):
            raise UserAlreadyExistsError(
                f"Username '{new_username}' already exists"
            )

        updated_user = await self.user_repository.update_by_username(
            old_username=old_username,
            new_username=new_username,
        )

        if updated_user is None:
            raise UserNotFoundError(
                "User not found"
            )

        return updated_user

    async def delete_user_account(
        self,
        user_id: UUID,
        password: str,
    ) -> User:

        user = await self.user_repository.get_by_id(
            user_id=user_id,
        )

        if user is None:
            raise UserNotFoundError(
                "User not found"
            )

        if not password_manager.verify(
            password,
            user.password,
        ):
            raise InvalidUsernamePassword(
                "Invalid username or password"
            )

        await self.user_repository.delete(
            user=user,
        )

        return user

    async def login(
        self,
        username: str,
        password: str,
    ) -> JWTResponsePayload:

        user = await self.user_repository.get_by_username(
            username
        )

        if user is None:
            raise InvalidUsernamePassword(
                "Invalid username or password"
            )

        if not password_manager.verify(
            password,
            user.password,
        ):
            raise InvalidUsernamePassword(
                "Invalid username or password"
            )

        return JWTHandler.generate(user.id)