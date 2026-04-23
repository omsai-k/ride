from __future__ import annotations

from typing import Protocol

from ride_backend.models import Device
from ride_backend.models import Participant
from ride_backend.models import RideSession
from ride_backend.models import User


class UserRepository(Protocol):
    def save(self, user: User) -> User: ...

    def get_by_id(self, user_id: str) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...


class DeviceRepository(Protocol):
    def save(self, device: Device) -> Device: ...

    def list_by_user_id(self, user_id: str) -> list[Device]: ...


class RideSessionRepository(Protocol):
    def save(self, session: RideSession) -> RideSession: ...

    def get_by_id(self, session_id: str) -> RideSession | None: ...

    def list_all(self) -> list[RideSession]: ...


class ParticipantRepository(Protocol):
    def save(self, participant: Participant) -> Participant: ...

    def list_by_session_id(self, ride_session_id: str) -> list[Participant]: ...

    def get_by_session_and_user(self, ride_session_id: str, user_id: str) -> Participant | None: ...
