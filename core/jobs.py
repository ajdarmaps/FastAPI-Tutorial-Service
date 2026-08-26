from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class JobStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


@dataclass
class Job:
    type: str
    payload: dict[str, Any]
    idempotency_key: str

    id: UUID = field(default_factory=uuid4)
    status: JobStatus = JobStatus.QUEUED
    attempts: int = 0
    max_attempts: int = 3
    last_error: str | None = None
    next_retry_delay: float | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
