from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions import (
    UserNotFoundError,
    InvalidUsernamePassword,
    UserAlreadyExistsError,
    PostNotFoundError,
)


async def user_not_found_handler(request: Request, exc: Exception):
    if isinstance(exc, UserNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


async def invalid_username_password_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    assert isinstance(exc, InvalidUsernamePassword)

    return JSONResponse(status_code=401, content={"detail": str(exc)})


async def user_already_exists_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    assert isinstance(exc, UserAlreadyExistsError)

    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
        },
    )


async def post_not_found_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


async def permission_denied_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc),
        },
    )
