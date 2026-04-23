from __future__ import annotations

import uuid
from datetime import UTC
from datetime import datetime

from ride_backend.errors import ConflictError
from ride_backend.errors import NotFoundError
from ride_backend.interfaces import DeviceRepository
from ride_backend.interfaces import ParticipantRepository
from ride_backend.interfaces import RideSessionRepository
from ride_backend.interfaces import UserRepository
from ride_backend.models import AudioEvent
from ride_backend.models import Device
from ride_backend.models import Message
from ride_backend.models import Participant
from ride_backend.models import RideSession
from ride_backend.models import User


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def get_me(self, user_id: str) -> User:
        user = self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    def update_me(self, user_id: str, display_name: str) -> User:
        user = self.get_me(user_id)
        updated = User(
            id=user.id,
            email=user.email,
            display_name=display_name,
            password_hash=user.password_hash,
            role=user.role,
        )
        return self._user_repo.save(updated)


class RideSessionService:
    def __init__(self, session_repo: RideSessionRepository) -> None:
        self._session_repo = session_repo

    def create(self, owner_user_id: str, title: str) -> RideSession:
        session = RideSession(id=str(uuid.uuid4()), owner_user_id=owner_user_id, title=title)
        return self._session_repo.save(session)

    def list_all(self) -> list[RideSession]:
        return self._session_repo.list_all()

    def update(self, session_id: str, title: str, status: str) -> RideSession:
        current = self._session_repo.get_by_id(session_id)
        if current is None:
            raise NotFoundError("Ride session not found")
        updated = RideSession(
            id=current.id,
            owner_user_id=current.owner_user_id,
            title=title,
            status=status,
        )
        return self._session_repo.save(updated)


class ParticipantService:
    def __init__(self, participant_repo: ParticipantRepository, session_repo: RideSessionRepository) -> None:
        self._participant_repo = participant_repo
        self._session_repo = session_repo

    def join(self, ride_session_id: str, user_id: str) -> Participant:
        session = self._session_repo.get_by_id(ride_session_id)
        if session is None:
            raise NotFoundError("Ride session not found")
        existing = self._participant_repo.get_by_session_and_user(ride_session_id, user_id)
        if existing is not None and existing.state == "joined":
            raise ConflictError("Participant already joined")
        participant = Participant(
            id=str(uuid.uuid4()),
            ride_session_id=ride_session_id,
            user_id=user_id,
            state="joined",
        )
        return self._participant_repo.save(participant)

    def leave(self, ride_session_id: str, user_id: str) -> Participant:
        participant = self._participant_repo.get_by_session_and_user(ride_session_id, user_id)
        if participant is None:
            raise NotFoundError("Participant not found")
        updated = Participant(
            id=participant.id,
            ride_session_id=participant.ride_session_id,
            user_id=participant.user_id,
            state="left",
        )
        return self._participant_repo.save(updated)

    def list_participants(self, ride_session_id: str) -> list[Participant]:
        return self._participant_repo.list_by_session_id(ride_session_id)


class DeviceService:
    def __init__(self, device_repo: DeviceRepository, user_repo: UserRepository) -> None:
        self._device_repo = device_repo
        self._user_repo = user_repo

    def register(self, user_id: str, platform: str, name: str) -> Device:
        user = self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        device = Device(id=str(uuid.uuid4()), user_id=user_id, platform=platform, name=name)
        return self._device_repo.save(device)

    def list_for_user(self, user_id: str) -> list[Device]:
        return self._device_repo.list_by_user_id(user_id)


class MessagingService:
    def send_message(self, ride_session_id: str, sender_user_id: str, body: str) -> Message:
        return Message(
            id=str(uuid.uuid4()),
            ride_session_id=ride_session_id,
            sender_user_id=sender_user_id,
            body=body,
            created_at=datetime.now(UTC),
        )

    def report_audio_event(self, ride_session_id: str, user_id: str, event_type: str) -> AudioEvent:
        return AudioEvent(
            id=str(uuid.uuid4()),
            ride_session_id=ride_session_id,
            user_id=user_id,
            event_type=event_type,
            created_at=datetime.now(UTC),
        )
