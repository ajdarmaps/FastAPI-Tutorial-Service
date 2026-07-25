from repositories.user_repository import UserRepository
from db.models import User
from core.hashing import password_manager
from exceptions import (
    UserNotFoundError,
    InvalidUsernamePassword,
    UserAlreadyExistsError,
)
from schema.output import UserOutput
from core.security import JWTHandler
from schema.jwt import JWTResponsePayload
from uuid import UUID


class UsersOperation:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, username: str, password: str) -> UserOutput:
        user_pwd = password_manager.hash(password)
        created_user = await self.user_repository.create(username, user_pwd)
        if created_user is None:
            raise UserAlreadyExistsError("Username already exists")
        return UserOutput.model_validate(created_user)

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
        user_id: UUID,
        password: str,
    ) -> User:
        user_delete = await self.user_repository.delete_user(
            user_id=user_id,
            password=password,
        )
        if user_delete is None:
            raise InvalidUsernamePassword("Invalid username or password")
        return user_delete

    async def login(
        self,
        username: str,
        password: str,
    ) -> JWTResponsePayload:
        user = await self.user_repository.get_by_username(username)
        if user is None:
            raise InvalidUsernamePassword("Invalid username or password")
        if not password_manager.verify(password, user.password):
            raise InvalidUsernamePassword("Invalid username or password")
        return JWTHandler.generate(user.id)
