import logging
from time import perf_counter
from uuid import uuid4
from core.config import settings


from fastapi import FastAPI, Request

from core.logging_config import configure_logging
from routers.users import router as user_router
from routers.posts import router as post_router
from exceptions.base import BaseAppException
from exceptions.handlers import app_exception_handler

configure_logging()

app = FastAPI(
    debug=settings.DEBUG,
)


logger = logging.getLogger(__name__)


@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next,
):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id

    started_at = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000

        logger.exception(
            "Unhandled request error: request_id=%s method=%s "
            "path=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            duration_ms,
        )

        raise

    duration_ms = (perf_counter() - started_at) * 1000

    logger.info(
        "HTTP request: request_id=%s method=%s path=%s "
        "status_code=%s duration_ms=%.2f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-ID"] = request_id

    return response


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
