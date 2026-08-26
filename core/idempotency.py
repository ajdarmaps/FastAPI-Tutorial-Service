from typing import Protocol


class IdempotencyStore(Protocol):

    async def has_succeeded(
        self,
        key: str,
    ) -> bool:
        ...

    async def mark_succeeded(
        self,
        key: str,
    ) -> None:
        ...


class InMemoryIdempotencyStore:

    def __init__(self) -> None:
        self._succeeded_keys: set[str] = set()

    async def has_succeeded(
        self,
        key: str,
    ) -> bool:
        return key in self._succeeded_keys

    async def mark_succeeded(
        self,
        key: str,
    ) -> None:
        self._succeeded_keys.add(key)
