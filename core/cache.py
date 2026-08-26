from typing import Any, Protocol, TypeVar
from time import monotonic
import logging

T = TypeVar("T")
logger = logging.getLogger(__name__)


class CacheBackend(Protocol):

    async def get(
        self,
        key: str,
    ) -> Any | None: ...

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int,
    ) -> None: ...

    async def delete(
        self,
        key: str,
    ) -> None: ...

    async def delete_prefix(
        self,
        prefix: str,
    ) -> None: ...


class InMemoryCache:

    def __init__(self) -> None:
        self._data: dict[str, tuple[Any, float]] = {}

    async def get(
        self,
        key: str,
    ) -> Any | None:
        item = self._data.get(key)

        if item is None:
            return None

        value, expires_at = item

        if monotonic() >= expires_at:
            self._data.pop(key, None)
            return None

        return value

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int,
    ) -> None:
        expires_at = monotonic() + ttl
        self._data[key] = (value, expires_at)

    async def delete(
        self,
        key: str,
    ) -> None:
        self._data.pop(key, None)

    async def delete_prefix(
        self,
        prefix: str,
    ) -> None:
        keys_to_delete = [key for key in self._data if key.startswith(prefix)]

        for key in keys_to_delete:
            self._data.pop(key, None)


async def get_or_set(
    cache: CacheBackend,
    key: str,
    factory,
    ttl: int,
) -> T:
    try:
        cached_value = await cache.get(key)
    except Exception:
        logger.warning(
            "Cache get failed for key=%s",
            key,
            exc_info=True,
        )
        return await factory()

    if cached_value is not None:
        return cached_value

    value = await factory()

    try:
        await cache.set(
            key=key,
            value=value,
            ttl=ttl,
        )
    except Exception:
        logger.warning(
            "Cache set failed for key=%s",
            key,
            exc_info=True,
        )

    return value
