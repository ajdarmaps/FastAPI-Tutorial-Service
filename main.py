from fastapi import FastAPI
from routers.users import router as user_router
from routers.posts import router as post_router

from exceptions import (
    UserNotFoundError,
    InvalidUsernamePassword,
    UserAlreadyExistsError,
    PostNotFoundError,
    PermissionDeniedError,
)
from exceptions.handlers import (
    user_not_found_handler,
    user_already_exists_handler,
    invalid_username_password_handler,
    post_not_found_handler,
    permission_denied_handler
)

app = FastAPI()

app.include_router(
    user_router,
    prefix="/api/users",
)
app.include_router(
    post_router,
    prefix="/api/posts",
)


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

app.add_exception_handler(
    PostNotFoundError,
    post_not_found_handler,
)

app.add_exception_handler(
    PermissionDeniedError,
    permission_denied_handler,
)
