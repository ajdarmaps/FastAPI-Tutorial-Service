from collections import deque
from typing import Protocol

from core.jobs import Job, JobStatus


class JobQueue(Protocol):

    async def enqueue(self, job: Job) -> None: ...

    async def dequeue(self) -> Job | None: ...


class InMemoryQueue:

    def __init__(self) -> None:
        self._queue: deque[Job] = deque()

    async def enqueue(self, job: Job) -> None:
        job.status = JobStatus.QUEUED
        self._queue.append(job)

    async def dequeue(self) -> Job | None:
        if not self._queue:
            return None

        job = self._queue.popleft()
        job.status = JobStatus.PROCESSING

        return job
