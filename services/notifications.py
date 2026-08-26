import logging

logger = logging.getLogger(__name__)


def send_welcome_notification(username: str) -> None:
    logger.info(
        "Welcome notification sent to username=%s",
        username,
    )
