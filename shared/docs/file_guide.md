# File Guide

This document is the quick map of the monorepo.

## Backend
- `backend/app/main.py`: FastAPI entrypoint.
- `backend/app/api/routes/`: REST endpoints.
- `backend/app/models/`: SQLAlchemy persistence layer.
- `backend/app/services/alert_engine.py`: rules-based alerts.
- `backend/app/services/anomaly.py`: personalized anomaly score.
- `backend/app/ml/inference.py`: model loading and prediction.
- `backend/app/db/seed.py`: demo seed.

## Web
- `apps/caregiver-web/app/dashboard/page.tsx`: main caregiver summary.
- `apps/caregiver-web/app/patients/page.tsx`: patient list.
- `apps/caregiver-web/app/patients/[id]/page.tsx`: individual patient detail.
- `apps/caregiver-web/app/alerts/page.tsx`: alert review table.
- `apps/caregiver-web/lib/api.ts`: API adapters + safe fallbacks.

## Mobile
- `apps/android-patient-app/app/src/main/java/.../MainActivity.kt`: Android entrypoint.
- `apps/android-patient-app/.../CogniWatchApp.kt`: Compose-based patient UI scaffold.
- `apps/android-patient-app/.../HealthConnectManager.kt`: health data integration placeholder.

## Wear OS
- `apps/wearos-module/.../MainActivity.kt`: wearable companion UI.

## ML
- `ml/src/models/train_darwin.py`: cognitive-motor model training.
- `ml/src/models/train_nacc_monitor.py`: monitoring tier model training.
- `ml/src/models/anomaly_engine.py`: anomaly logic.
- `ml/src/serving/risk_service.py`: serving wrapper.
