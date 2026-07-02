# Security and Privacy Notes

## Included protections
- JWT authentication.
- Role-based access control.
- Password hashing with bcrypt.
- CORS configuration.
- Consent flag on patient profile.
- Alert and note separation from authentication layer.
- Health data collection limited to necessary minimums.

## Recommended next steps for a stronger thesis-to-product path
- Add refresh tokens.
- Add audit trails for alert state changes.
- Encrypt secrets with a secret manager in production.
- Add database-level row ownership policies if moving to Supabase or advanced PostgreSQL roles.
- Add full FCM credential handling for device tokens.
- Add legal review for privacy notices and consent copy.
