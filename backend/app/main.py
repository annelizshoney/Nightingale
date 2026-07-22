from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.utils.logger import logger

from app.api.v1.routes.dashboard import router as dashboard_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.medication import router as medication_router
from app.api.v1.routes.memory import router as memory_router
from app.api.v1.routes.alerts import router as alerts_router
from app.api.v1.routes.family import router as family_router
from app.api.v1.routes.doctor import router as doctor_router

logger.info("Starting Nightingale Backend")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response


app.include_router(dashboard_router, prefix=settings.API_PREFIX)
app.include_router(health_router, prefix=settings.API_PREFIX)
app.include_router(medication_router, prefix=settings.API_PREFIX)
app.include_router(memory_router, prefix=settings.API_PREFIX)
app.include_router(alerts_router, prefix=settings.API_PREFIX)
app.include_router(family_router, prefix=settings.API_PREFIX)
app.include_router(doctor_router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {
        "success": True,
        "message": f"{settings.APP_NAME} Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }