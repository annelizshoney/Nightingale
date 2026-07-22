import logging

from app.core.settings import settings


logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(settings.APP_NAME)