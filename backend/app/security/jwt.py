from datetime import datetime, timezone
from datetime import timedelta

from jose import jwt

from app.core.settings import settings

ALGORITHM = "HS256"


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.now(timezone.utc) + timedelta(days=1)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )