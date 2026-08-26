from collections.abc import Awaitable, Callable
from core.retry import calculate_backoff

from core.jobs import Job, JobStatus
from core.queue import JobQueue
from core.idempotency import IdempotencyStore

JobHandler = Callable[
    [Job],
    Awaitable[None],
]


class InMemoryWorker:

    def __init__(
        self,
        queue: JobQueue,
        handlers: dict[str, JobHandler],
        idempotency_store: IdempotencyStore,
    ) -> None:
        self.queue = queue
        self.handlers = handlers
        self.idempotency_store = idempotency_store

    async def run_once(self) -> Job | None:
        job = await self.queue.dequeue()

        if job is None:
            return None
        already_succeeded = await self.idempotency_store.has_succeeded(
            job.idempotency_key
        )
        if already_succeeded:
            job.status = JobStatus.COMPLETED
            return job

        handler = self.handlers.get(job.type)

        if handler is None:
            job.status = JobStatus.DEAD_LETTER
            job.last_error = f"No handler registered for job type: {job.type}"
            return job

        try:
            await handler(job)

        except Exception as exc:
            job.attempts += 1
            job.last_error = str(exc)

            job.next_retry_delay = calculate_backoff(
                attempt=job.attempts,
            )

            if job.attempts < job.max_attempts:
                job.status = JobStatus.QUEUED
                await self.queue.enqueue(job)
            else:
                job.status = JobStatus.DEAD_LETTER

        else:
            await self.idempotency_store.mark_succeeded(
                job.idempotency_key
            )

            job.status = JobStatus.COMPLETED

        return job
