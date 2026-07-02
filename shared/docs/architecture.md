# Architecture Decision Record

## Final product positioning

CogniWatch is a **monitoring and support platform**, not a diagnostic medical device.

## Core architectural decision

Use a **hybrid evidence stack**:

- **Wear OS + Health Services** for near-device collection.
- **Health Connect** on Android as the main mobile health aggregation layer.
- **FastAPI + PostgreSQL/Neon** for backend and persistence.
- **Next.js caregiver dashboard** for oversight.
- **Two analytical layers** instead of forcing one dataset into one model.

## Why the uploaded datasets forced this decision

### DARWIN
- Small dataset.
- Cross-sectional.
- Digital handwriting / fine motor task features.
- Strong for **proxy cognitive-motor screening**, weak for passive longitudinal wearable monitoring.

### NACC
- Large research dataset.
- Longitudinal clinical and functional observations.
- Strong for designing a **monitoring tier model** and intake/baseline logic.
- Not directly wearable telemetry, so it should not be misrepresented as smartwatch training data.

## Final analytics design

### Model A: DARWIN cognitive-motor proxy
Input: touch / trace task features from the smartphone app.
Output: probability-like risk flag for deviation in fine motor/cognitive behavior.
Purpose: complement, not diagnose.

### Model B: NACC-based monitoring tier model
Input: intake/baseline features, brief scales, self-report proxies, function and cognitive task proxies.
Output: `low_monitoring`, `watchlist`, `high_support`.
Purpose: baseline tiering for follow-up intensity.

### Model C: personalized anomaly scoring
Input: daily wearable summaries.
Output: anomaly score against personal baseline.
Purpose: generate explainable daily alerts.

## Data flow

1. Patient completes onboarding.
2. Consent is stored.
3. Wearable is linked.
4. Phone app reads Health Connect and aggregates daily summaries.
5. Optional microassessment sends derived task features.
6. Backend combines baseline tier + anomaly score + cognitive-motor probability.
7. Caregiver sees alerts and trends.
