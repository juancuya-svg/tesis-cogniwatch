# CogniWatch Thesis Project

CogniWatch is a thesis-ready digital health platform for **functional and cognitive monitoring**. It is not positioned as a diagnostic device. Instead, it combines:

- **Longitudinal wearable monitoring** from Wear OS + Health Connect.
- **Caregiver-friendly tracking** of sleep, activity, heart metrics, adherence, check-ins, and alerts.
- **A cognitive-motor microassessment layer** inspired by the DARWIN handwriting dataset, adapted for smartphone touch interaction.
- **A monitoring-tier model** trained from NACC clinical data and adapted into non-diagnostic support levels.
- **A hybrid rules + ML alert engine** that compares patients against their own baseline.

## Why this architecture

The uploaded data led to a better product decision than a “smartwatch-only Alzheimer app”:

1. **DARWIN** is not smartwatch telemetry. It is a small, high-dimensional cognitive-motor dataset built from 25 digital handwriting tasks. It is best used as an **initial or follow-up microassessment module** inside the patient app.
2. **NACC** is large, longitudinal, and much stronger for defining a **baseline monitoring profile** and support-tier engine.
3. Wearables are strongest for **continuous observation** (sleep, steps, heart rate, inactivity, adherence, longitudinal drift).

The result is a **hybrid platform**:

- **Phone app**: onboarding, consent, caregiver linking, self-reports, optional drawing/tapping microtasks, Health Connect permissioning, summary view.
- **Wear OS app**: passive data collection and sync cues.
- **Backend**: JWT auth, role-based access, patient/caregiver relationships, daily summaries, alerts, notes, monitoring scores.
- **Caregiver web dashboard**: patients, trends, alerts, notes, support tier.
- **ML layer**:
  - DARWIN-based cognitive-motor proxy model.
  - NACC-based monitoring tier model.
  - Personalized anomaly scoring for daily wearable signals.

## Monorepo structure

```text
/apps
  /android-patient-app
  /wearos-module
  /caregiver-web
  /admin-console
/backend
/ml
/shared
/infra
/data
```

## What is production-ready vs. thesis-ready

This repository is **thesis-ready and development-ready**:

- Backend code is executable.
- Dockerized local stack is included.
- ML training and inference scripts are included.
- Web dashboard is source-ready.
- Android and Wear OS modules are source-ready and organized for Android Studio.

Because this environment does not ship Android SDKs, an APK/AAB was not compiled here. Source code and project files are included so you can open them directly in Android Studio.

## Recommended smartwatch

**Primary low-cost reference device**: Samsung Galaxy Watch FE.

Why:
- Wear OS device available in Peru.
- Sleep, heart and activity tracking coverage is enough for this thesis.
- Lower cost than Pixel Watch while still aligning with the requested stack.
- Good fit for Health Services + phone-side Health Connect strategy.

**Premium reference device**: Pixel Watch 3, if budget allows and you want Google-first testing.

## Quick start

### 1) Run backend + database + caregiver web

```bash
docker compose up --build
```

Services:
- API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Caregiver web: http://localhost:3000
- PostgreSQL: localhost:5432

### 2) Seed demo data

```bash
docker compose exec backend python -m app.db.seed
```

### 3) Train / refresh ML artifacts

```bash
python ml/src/models/train_darwin.py
python ml/src/models/train_nacc_monitor.py
```

### 4) Open mobile apps

- Open `apps/android-patient-app` in Android Studio.
- Open `apps/wearos-module` in Android Studio.

## Demo credentials

After seeding:
- Caregiver: `caregiver@cogniwatch.local` / `ChangeMe123!`
- Patient: `patient@cogniwatch.local` / `ChangeMe123!`
- Admin: `admin@cogniwatch.local` / `ChangeMe123!`

## Key thesis message

This project should be presented as:

> A configurable digital monitoring platform for functional and cognitive change detection using wearable signals, caregiver observation, self-report, and optional cognitive-motor microassessments.

It should **not** be presented as medical diagnosis software.
