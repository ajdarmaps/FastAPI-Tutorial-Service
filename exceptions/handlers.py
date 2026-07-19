from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions import UserNotFoundError, InvalidUsernamePassword


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
