# Backend API Reference

## Authentication
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

## Patients
- `POST /api/v1/patients`
- `GET /api/v1/patients`
- `GET /api/v1/patients/{patient_id}/overview`
- `POST /api/v1/patients/{patient_id}/baseline`
- `POST /api/v1/patients/{patient_id}/signals/daily`
- `POST /api/v1/patients/{patient_id}/cognitive-motor`
- `GET /api/v1/patients/{patient_id}/alerts`

## Alerts
- `GET /api/v1/alerts`
- `PATCH /api/v1/alerts/{alert_id}/status?status=viewed`

## Admin
- `GET /api/v1/admin/summary`
