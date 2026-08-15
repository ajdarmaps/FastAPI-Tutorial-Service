from fastapi import FastAPI

from routers.users import router as user_router
from routers.posts import router as post_router

from exceptions.base import BaseAppException
from exceptions.handlers import app_exception_handler

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
    BaseAppException,
    app_exception_handler,
)
