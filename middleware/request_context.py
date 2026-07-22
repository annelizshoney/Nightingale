from __future__ import annotations

import time
from typing import Callable
from uuid import uuid4

from fastapi import Request
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.context import request_id_context
from app.core.settings import settings
from app.utils.logger import logger


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        token = request_id_context.set(request_id)
        tracer = trace.get_tracer(settings.OTEL_SERVICE_NAME)
        start = time.perf_counter()

        with tracer.start_as_current_span(f"http.{request.method.lower()}") as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.target", request.url.path)
            span.set_attribute("http.request_id", request_id)
            request.state.request_id = request_id
            logger.info("Incoming request %s %s", request.method, request.url.path)
            try:
                response = await call_next(request)
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                logger.exception("Request failed %s %s", request.method, request.url.path)
                raise
            finally:
                request_id_context.reset(token)

            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            span.set_attribute("http.duration_ms", duration_ms)

        response.headers["X-Request-ID"] = request_id
        logger.info("Completed request %s %s in %sms", request.method, request.url.path, duration_ms)
        return response
