import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.base import BaseAppException

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, BaseAppException)

    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        "Application error: request_id=%s method=%s path=%s "
        "status_code=%s exception=%s",
        request_id,
        request.method,
        request.url.path,
        exc.status_code,
        type(exc).__name__,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )
