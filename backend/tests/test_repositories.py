from ride_backend.models import Device
from ride_backend.models import Participant
from ride_backend.models import RideSession
from ride_backend.models import User
from ride_backend.repositories import InMemoryDeviceRepository
from ride_backend.repositories import InMemoryParticipantRepository
from ride_backend.repositories import InMemoryRideSessionRepository
from ride_backend.repositories import InMemoryUserRepository


def test_user_repository_save_and_get() -> None:
    repo = InMemoryUserRepository()
    user = User(id="u1", email="rider@example.com", display_name="Rider", password_hash="hash")
    repo.save(user)

    assert repo.get_by_id("u1") == user
    assert repo.get_by_email("rider@example.com") == user
    assert repo.get_by_email("missing@example.com") is None


def test_device_repository_lists_by_user() -> None:
    repo = InMemoryDeviceRepository()
    d1 = Device(id="d1", user_id="u1", platform="android", name="Phone")
    d2 = Device(id="d2", user_id="u1", platform="ios", name="Backup")
    repo.save(d1)
    repo.save(d2)

    assert repo.list_by_user_id("u1") == [d1, d2]
    assert repo.list_by_user_id("u2") == []


def test_ride_session_repository() -> None:
    repo = InMemoryRideSessionRepository()
    session = RideSession(id="s1", owner_user_id="u1", title="Morning")
    repo.save(session)

    assert repo.get_by_id("s1") == session
    assert repo.list_all() == [session]


def test_participant_repository() -> None:
    repo = InMemoryParticipantRepository()
    p1 = Participant(id="p1", ride_session_id="s1", user_id="u1")
    p2 = Participant(id="p2", ride_session_id="s1", user_id="u2")
    repo.save(p1)
    repo.save(p2)

    assert repo.get_by_session_and_user("s1", "u1") == p1
    assert repo.list_by_session_id("s1") == [p1, p2]
    assert repo.get_by_session_and_user("s2", "u1") is None
