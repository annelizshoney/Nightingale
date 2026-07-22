from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.routes.alerts import router as alerts_router
from app.api.v1.routes.appointment import router as appointment_router
from app.api.v1.routes.dashboard import router as dashboard_router
from app.api.v1.routes.doctor import router as doctor_router
from app.api.v1.routes.emergency import router as emergency_router
from app.api.v1.routes.family import router as family_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.medication import router as medication_router
from app.api.v1.routes.memory import router as memory_router
from app.api.v1.routes.orchestrator import router as orchestrator_router
from app.api.v1.routes.routine import router as routine_router
from app.core.exception_handlers import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.settings import settings
from app.core.tracing import configure_tracing
from app.db.base import Base
from app.db.database import engine
from app.core.dependencies import (
    get_adk_client,
    get_agent_registry,
    get_lyzr_client,
    get_lyzr_orchestrator,
    get_prompt_repository,
    get_qdrant_client,
)
from app.middleware.request_context import RequestContextMiddleware
from app.utils.logger import logger


def _parse_origins(raw_origins: str) -> list[str]:
    if raw_origins.strip() == "*":
        return ["*"]
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def _bootstrap_runtime() -> None:
    configure_tracing()
    Base.metadata.create_all(bind=engine)
    get_qdrant_client()
    get_adk_client()
    get_lyzr_client()
    get_agent_registry()
    get_lyzr_orchestrator()
    get_prompt_repository()
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Bootstrapping Nightingale runtime")
    _bootstrap_runtime()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_parse_origins(settings.CORS_ALLOW_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(dashboard_router, prefix=settings.API_PREFIX)
    app.include_router(health_router, prefix=settings.API_PREFIX)
    app.include_router(medication_router, prefix=settings.API_PREFIX)
    app.include_router(memory_router, prefix=settings.API_PREFIX)
    app.include_router(alerts_router, prefix=settings.API_PREFIX)
    app.include_router(family_router, prefix=settings.API_PREFIX)
    app.include_router(doctor_router, prefix=settings.API_PREFIX)
    app.include_router(appointment_router, prefix=settings.API_PREFIX)
    app.include_router(routine_router, prefix=settings.API_PREFIX)
    app.include_router(emergency_router, prefix=settings.API_PREFIX)
    app.include_router(orchestrator_router, prefix=settings.API_PREFIX)

    @app.get("/")
    def root() -> dict[str, object]:
        return {
            "success": True,
            "message": f"{settings.APP_NAME} Backend Running",
        }

    return app
