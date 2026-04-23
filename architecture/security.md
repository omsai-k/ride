# Security & Privacy

## Authentication
- JWT-based authentication for all endpoints
- Refresh tokens for session management
- Device binding for additional security

## Authorization
- Role-based access (user, admin)
- Session-level permissions (admin/member)

## Data Protection
- HTTPS for all API and signaling traffic
- DTLS-SRTP for RTC media encryption
- Passwords hashed with bcrypt/argon2
- Sensitive data (tokens, keys) stored securely

## Privacy
- Minimal data collection (only required for operation)
- User data never shared with third parties
- Users can delete account and all associated data

## Logging & Monitoring
- Audit logs for admin actions
- Anomaly detection for abuse
- Alerting for suspicious activity

## Compliance
- GDPR-ready data handling
- Extensible for other privacy regulations
