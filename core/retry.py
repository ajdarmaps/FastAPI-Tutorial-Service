def calculate_backoff(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
) -> float:
    if attempt < 1:
        raise ValueError("attempt must be greater than zero")

    delay = base_delay * (2 ** (attempt - 1))

    return min(delay, max_delay)
