# Data Models

## User
- id: UUID (PK)
- username: string (unique)
- email: string (unique, optional)
- phone: string (unique, optional)
- password_hash: string
- avatar_url: string
- created_at: timestamp
- updated_at: timestamp
- device_info: JSON
- platform: enum (android, ios)
- helmet_model: string (optional)

## RideSession
- id: UUID (PK)
- name: string
- created_by: UUID (FK → User)
- created_at: timestamp
- is_active: boolean
- session_type: enum (group, solo)
- participants: [UUID] (User IDs)
- rtc_room_id: string

## Participant
- id: UUID (PK)
- user_id: UUID (FK → User)
- session_id: UUID (FK → RideSession)
- joined_at: timestamp
- left_at: timestamp (nullable)
- role: enum (admin, member)
- is_muted: boolean

## Message (for signaling, chat, or system events)
- id: UUID (PK)
- session_id: UUID (FK → RideSession)
- sender_id: UUID (FK → User)
- type: enum (text, system, signal)
- content: string (JSON for signal/system)
- created_at: timestamp

## Device
- id: UUID (PK)
- user_id: UUID (FK → User)
- device_id: string
- platform: enum (android, ios)
- helmet_model: string
- bluetooth_address: string
- last_seen: timestamp

## AudioEvent
- id: UUID (PK)
- session_id: UUID (FK → RideSession)
- user_id: UUID (FK → User)
- event_type: enum (voice_start, voice_end, music_start, music_end, bt_switch)
- timestamp: timestamp
- metadata: JSON

## RTCSession
- id: UUID (PK)
- rtc_room_id: string
- session_id: UUID (FK → RideSession)
- started_at: timestamp
- ended_at: timestamp (nullable)
- active_participants: [UUID]

## Table Relationships
- User 1—* Device
- User 1—* Participant
- RideSession 1—* Participant
- RideSession 1—* Message
- RideSession 1—* AudioEvent
- RideSession 1—1 RTCSession

## Notes
- All UUIDs are v4.
- Timestamps are UTC.
- Extendable for future features (location, ride recording, etc).
