from ride_backend.interfaces import DeviceRepository
from ride_backend.interfaces import ParticipantRepository
from ride_backend.interfaces import RideSessionRepository
from ride_backend.interfaces import UserRepository
from ride_backend.models import Device
from ride_backend.models import Participant
from ride_backend.models import RideSession
from ride_backend.models import User


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, User] = {}
        self._email_to_id: dict[str, str] = {}

    def save(self, user: User) -> User:
        self._by_id[user.id] = user
        self._email_to_id[user.email] = user.id
        return user

    def get_by_id(self, user_id: str) -> User | None:
        return self._by_id.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        user_id = self._email_to_id.get(email)
        if user_id is None:
            return None
        return self._by_id.get(user_id)


class InMemoryDeviceRepository(DeviceRepository):
    def __init__(self) -> None:
        self._by_user: dict[str, list[Device]] = {}

    def save(self, device: Device) -> Device:
        devices = self._by_user.setdefault(device.user_id, [])
        devices.append(device)
        return device

    def list_by_user_id(self, user_id: str) -> list[Device]:
        return list(self._by_user.get(user_id, []))


class InMemoryRideSessionRepository(RideSessionRepository):
    def __init__(self) -> None:
        self._sessions: dict[str, RideSession] = {}

    def save(self, session: RideSession) -> RideSession:
        self._sessions[session.id] = session
        return session

    def get_by_id(self, session_id: str) -> RideSession | None:
        return self._sessions.get(session_id)

    def list_all(self) -> list[RideSession]:
        return list(self._sessions.values())


class InMemoryParticipantRepository(ParticipantRepository):
    def __init__(self) -> None:
        self._participants: dict[str, Participant] = {}

    def save(self, participant: Participant) -> Participant:
        key = self._key(participant.ride_session_id, participant.user_id)
        self._participants[key] = participant
        return participant

    def list_by_session_id(self, ride_session_id: str) -> list[Participant]:
        return [
            participant
            for participant in self._participants.values()
            if participant.ride_session_id == ride_session_id
        ]

    def get_by_session_and_user(self, ride_session_id: str, user_id: str) -> Participant | None:
        return self._participants.get(self._key(ride_session_id, user_id))

    @staticmethod
    def _key(ride_session_id: str, user_id: str) -> str:
        return f"{ride_session_id}:{user_id}"
