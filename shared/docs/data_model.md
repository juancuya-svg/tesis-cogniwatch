# Data Model Summary

## Core entities

- `users`
- `patient_profiles`
- `caregiver_links`
- `baseline_assessments`
- `wearable_daily_summaries`
- `cognitive_motor_sessions`
- `alerts`
- `care_notes`

## Key business rules

1. A user can have one role: patient, caregiver, clinician or admin.
2. A patient can be linked to one or many caregivers.
3. A patient has one mutable profile and many observations over time.
4. Alerts are event-like objects derived from baseline comparison and score logic.
5. Missing wearable signals are acceptable and expected.
6. Cognitive-motor sessions are optional.
7. Monitoring tier is non-diagnostic and used only for follow-up intensity.
