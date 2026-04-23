from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: str
    email: str
    display_name: str
    password_hash: str
    role: str = "rider"


@dataclass(frozen=True)
class Device:
    id: str
    user_id: str
    platform: str
    name: str


@dataclass(frozen=True)
class RideSession:
    id: str
    owner_user_id: str
    title: str
    status: str = "active"


@dataclass(frozen=True)
class Participant:
    id: str
    ride_session_id: str
    user_id: str
    state: str = "joined"


@dataclass(frozen=True)
class Message:
    id: str
    ride_session_id: str
    sender_user_id: str
    body: str
    created_at: datetime


@dataclass(frozen=True)
class AudioEvent:
    id: str
    ride_session_id: str
    user_id: str
    event_type: str
    created_at: datetime


@dataclass(frozen=True)
class RtcSession:
    id: str
    ride_session_id: str
    room_id: str
    state: str = "open"
