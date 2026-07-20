from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.engine import Base, engine
from routers.users import router as user_router

from exceptions import (
    UserNotFoundError,
    InvalidUsernamePassword,
    UserAlreadyExistsError,
)
from exceptions.handlers import (
    user_not_found_handler,
    user_already_exists_handler,
    invalid_username_password_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users")

app.add_exception_handler(
    UserNotFoundError,
    user_not_found_handler,
)

app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)

app.add_exception_handler(
    InvalidUsernamePassword,
    invalid_username_password_handler,
)
