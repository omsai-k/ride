-- Phase 2 initial schema

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'rider',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE devices (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_devices_user_id ON devices(user_id);

CREATE TABLE ride_sessions (
    id UUID PRIMARY KEY,
    owner_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_ride_sessions_owner_user_id ON ride_sessions(owner_user_id);

CREATE TABLE participants (
    id UUID PRIMARY KEY,
    ride_session_id UUID NOT NULL REFERENCES ride_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    state TEXT NOT NULL DEFAULT 'joined',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (ride_session_id, user_id)
);
CREATE INDEX idx_participants_ride_session_id ON participants(ride_session_id);

CREATE TABLE messages (
    id UUID PRIMARY KEY,
    ride_session_id UUID NOT NULL REFERENCES ride_sessions(id) ON DELETE CASCADE,
    sender_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_messages_ride_session_id ON messages(ride_session_id);

CREATE TABLE audio_events (
    id UUID PRIMARY KEY,
    ride_session_id UUID NOT NULL REFERENCES ride_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_audio_events_ride_session_id ON audio_events(ride_session_id);

CREATE TABLE rtc_sessions (
    id UUID PRIMARY KEY,
    ride_session_id UUID NOT NULL REFERENCES ride_sessions(id) ON DELETE CASCADE,
    room_id TEXT NOT NULL UNIQUE,
    state TEXT NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_rtc_sessions_ride_session_id ON rtc_sessions(ride_session_id);
