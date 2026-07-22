from fastapi import FastAPI

from app.api.v1.routes.dashboard import router as dashboard_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.medication import router as medication_router
from app.api.v1.routes.memory import router as memory_router
from app.api.v1.routes.alerts import router as alerts_router
from app.api.v1.routes.family import router as family_router
from app.api.v1.routes.doctor import router as doctor_router

app = FastAPI(
    title="Nightingale API",
    version="1.0.0",
)

app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(medication_router, prefix="/api/v1")
app.include_router(memory_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(family_router, prefix="/api/v1")
app.include_router(doctor_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Nightingale Backend Running"
    }