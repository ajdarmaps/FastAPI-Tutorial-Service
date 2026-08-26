from typing import Annotated

from fastapi import Depends

from core.cache import CacheBackend, InMemoryCache


cache = InMemoryCache()


def get_cache() -> CacheBackend:
    return cache


CacheDep = Annotated[
    CacheBackend,
    Depends(get_cache),
]
