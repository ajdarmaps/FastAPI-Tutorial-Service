from uuid import UUID

from core.hashing import password_manager
from core.security import JWTHandler
from db.models import User
from exceptions import (
    InvalidUsernamePassword,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from schema.jwt import JWTResponsePayload
from unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from sqlalchemy.exc import IntegrityError


class UsersOperation:

    def __init__(
        self,
        uow: SQLAlchemyUnitOfWork,
    ):
        self.uow = uow

    async def create(
        self,
        username: str,
        password: str,
    ) -> User:

        hashed_password = password_manager.hash(password)

        try:
            async with self.uow:
                existing_user = await self.uow.users.get_by_username(username)

                if existing_user is not None:
                    raise UserAlreadyExistsError("Username already exists")

                user = await self.uow.users.create(
                    username=username,
                    password=hashed_password,
                )

                await self.uow.commit()

        except IntegrityError as exc:
            raise UserAlreadyExistsError("Username already exists") from exc

        return user

    async def get_user_by_username(
        self,
        username: str,
    ) -> User:

        user = await self.uow.users.get_by_username(username)

        if user is None:
            raise UserNotFoundError("User not found")

        return user

    async def update_user_profile(
        self,
        old_username: str,
        new_username: str,
    ) -> User:
        try:
            async with self.uow:
                user = await self.uow.users.get_by_username(old_username)

                if user is None:
                    raise UserNotFoundError("User not found")

                existing_user = await self.uow.users.get_by_username(new_username)

                if existing_user is not None and existing_user.id != user.id:
                    raise UserAlreadyExistsError(
                        f"Username '{new_username}' already exists"
                    )

                updated_user = await self.uow.users.update_by_username(
                    old_username=old_username,
                    new_username=new_username,
                )

                if updated_user is None:
                    raise UserNotFoundError("User not found")

                await self.uow.commit()

        except IntegrityError as exc:
            raise UserAlreadyExistsError(
                f"Username '{new_username}' already exists"
            ) from exc

        return updated_user

    async def delete_user_account(
        self,
        user_id: UUID,
        password: str,
    ) -> User:

        async with self.uow:
            user = await self.uow.users.get_by_id(user_id=user_id)

            if user is None:
                raise UserNotFoundError("User not found")

            if not password_manager.verify(password, user.password):
                raise InvalidUsernamePassword("Invalid username or password")

            await self.uow.users.delete(user=user)
            await self.uow.commit()

        return user

    async def login(
        self,
        username: str,
        password: str,
    ) -> JWTResponsePayload:

        user = await self.uow.users.get_by_username(username)

        if user is None:
            raise InvalidUsernamePassword("Invalid username or password")

        if not password_manager.verify(
            password,
            user.password,
        ):
            raise InvalidUsernamePassword("Invalid username or password")

        return JWTHandler.generate(user.id)

    async def get_all_users(self) -> list[User]:
        return await self.uow.users.list_users()
