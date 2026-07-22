from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.core.context import get_request_id
from app.utils.logger import logger


def _error_payload(detail: str, *, code: str, extra: dict | None = None) -> dict:
    payload = {
        "success": False,
        "error": {
            "code": code,
            "message": detail,
            "request_id": get_request_id(),
        },
    }
    if extra:
        payload["error"]["details"] = extra
    return payload


async def http_exception_handler(request: Request, exc):
    logger.warning("HTTP error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        content=_error_payload(str(getattr(exc, "detail", exc)), code="http_error"),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=_error_payload("Request validation failed", code="validation_error", extra={"errors": exc.errors()}),
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=_error_payload("Internal server error", code="internal_error"),
    )
