from repositories.user_repository import UserRepository
from db.models import User
from core.security import password_manager
from exceptions import (
    UserNotFoundError,
    InvalidUsernamePassword,
    UserAlreadyExistsError,
)
from schema.output import RegisterOutput


class UsersOperation:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, username: str, password: str) -> RegisterOutput:
        user_pwd = password_manager.hash(password)
        created_user = await self.user_repository.create(username, user_pwd)
        if created_user is None:
            raise UserAlreadyExistsError("Username already exists")
        return RegisterOutput.model_validate(created_user)

    async def get_user_by_username(self, username: str) -> User:
        user = await self.user_repository.get_by_username(username)
        if user is None:
            raise UserNotFoundError("User not found")
        return user

    async def update_user_profile(
        self,
        old_username: str,
        new_username: str,
    ) -> User | None:
        user_update = await self.user_repository.update_by_username(
            old_username=old_username, new_username=new_username
        )
        if user_update is None:
            raise UserNotFoundError("User not found")
        return user_update

    async def delete_user_account(
        self,
        username: str,
        password: str,
    ) -> User:
        user_delete = await self.user_repository.delete_user(
            username=username,
            password=password,
        )
        if user_delete is None:
            raise InvalidUsernamePassword("Invalid username or password")
        return user_delete
