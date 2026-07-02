from fastapi import APIRouter

from app.api.routes import auth, patients, alerts, signals, assessments, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(signals.router, prefix="/signals", tags=["signals"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
