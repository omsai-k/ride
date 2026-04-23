# API Design

## Authentication
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- POST /auth/refresh

## User
- GET /user/me
- PATCH /user/me
- GET /user/{id}
- GET /user/search?q=...

## Ride Sessions
- POST /ridesession
- GET /ridesession/{id}
- GET /ridesession/active
- PATCH /ridesession/{id}
- DELETE /ridesession/{id}
- POST /ridesession/{id}/join
- POST /ridesession/{id}/leave

## Participants
- GET /ridesession/{id}/participants
- PATCH /participant/{id}
- DELETE /participant/{id}

## Messaging
- GET /ridesession/{id}/messages
- POST /ridesession/{id}/message

## Device
- POST /device/register
- GET /device/my
- PATCH /device/{id}
- DELETE /device/{id}

## RTC Signaling (WebSocket)
- /ws/rtc/{rtc_room_id}
  - join, leave, offer, answer, ice-candidate, mute, unmute, etc.

## Audio Events
- POST /ridesession/{id}/audioevent
- GET /ridesession/{id}/audioevents

## Admin
- GET /admin/stats
- GET /admin/logs

## Notes
- All endpoints require JWT auth unless public.
- REST for CRUD, WebSocket for RTC signaling.
- Extendable for future features (location, ride recording, etc).
