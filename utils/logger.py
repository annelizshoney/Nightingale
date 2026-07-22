import logging

from app.core.context import get_request_id
from app.core.settings import settings


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(request_id)s | %(message)s",
)

logger = logging.getLogger(settings.APP_NAME)
logger.addFilter(RequestContextFilter())