# Smartwatch Decision

## Recommended thesis device

### Primary recommendation: Samsung Galaxy Watch FE

Why it wins for this thesis:
- Lower entry cost than Pixel Watch.
- Officially available in Peru.
- Wear OS support aligns with requested stack.
- Tracks sleep, heart health and activity well enough for the thesis scope.
- Realistic device for a low-cost academic prototype.

## Secondary recommendation: Pixel Watch 3

Use this if:
- Budget is less constrained.
- You want a Google-first reference environment.
- You prefer more direct alignment with Google ecosystem testing.

## Practical engineering note

The thesis architecture does **not depend on brand-exclusive data**. The safest implementation path is:
- Collect on-device metrics with **Health Services** when relevant.
- Read aggregated records on the phone with **Health Connect**.
- Design graceful fallbacks when some signals are missing.
