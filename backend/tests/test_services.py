import pytest

from ride_backend.errors import ConflictError
from ride_backend.errors import NotFoundError
from ride_backend.models import RideSession
from ride_backend.models import User
from ride_backend.repositories import InMemoryDeviceRepository
from ride_backend.repositories import InMemoryParticipantRepository
from ride_backend.repositories import InMemoryRideSessionRepository
from ride_backend.repositories import InMemoryUserRepository
from ride_backend.services import DeviceService
from ride_backend.services import MessagingService
from ride_backend.services import ParticipantService
from ride_backend.services import RideSessionService
from ride_backend.services import UserService


def test_user_service_get_and_update() -> None:
    users = InMemoryUserRepository()
    users.save(User(id="u1", email="rider@example.com", display_name="Rider", password_hash="h"))
    service = UserService(users)

    me = service.get_me("u1")
    updated = service.update_me("u1", "Captain")

    assert me.display_name == "Rider"
    assert updated.display_name == "Captain"


def test_user_service_not_found() -> None:
    service = UserService(InMemoryUserRepository())
    with pytest.raises(NotFoundError):
        service.get_me("missing")


def test_ride_session_service_create_list_update() -> None:
    repo = InMemoryRideSessionRepository()
    service = RideSessionService(repo)

    created = service.create("u1", "Morning")
    updated = service.update(created.id, "Evening", "active")

    assert service.list_all()[0].id == created.id
    assert updated.title == "Evening"


def test_ride_session_service_update_missing() -> None:
    service = RideSessionService(InMemoryRideSessionRepository())
    with pytest.raises(NotFoundError):
        service.update("missing", "x", "active")


def test_participant_join_leave_list() -> None:
    sessions = InMemoryRideSessionRepository()
    sessions.save(RideSession(id="s1", owner_user_id="u1", title="Ride"))

    participants = InMemoryParticipantRepository()
    service = ParticipantService(participants, sessions)

    joined = service.join("s1", "u2")
    left = service.leave("s1", "u2")

    assert joined.state == "joined"
    assert left.state == "left"
    assert len(service.list_participants("s1")) == 1


def test_participant_join_conflict_and_missing() -> None:
    sessions = InMemoryRideSessionRepository()
    sessions.save(RideSession(id="s1", owner_user_id="u1", title="Ride"))
    participants = InMemoryParticipantRepository()
    service = ParticipantService(participants, sessions)

    service.join("s1", "u2")
    with pytest.raises(ConflictError):
        service.join("s1", "u2")

    with pytest.raises(NotFoundError):
        service.join("missing", "u2")


def test_device_service_register_and_list() -> None:
    users = InMemoryUserRepository()
    users.save(User(id="u1", email="rider@example.com", display_name="R", password_hash="h"))
    devices = InMemoryDeviceRepository()
    service = DeviceService(devices, users)

    device = service.register("u1", "android", "Pixel")

    assert device.platform == "android"
    assert service.list_for_user("u1")[0].name == "Pixel"


def test_device_service_register_missing_user() -> None:
    service = DeviceService(InMemoryDeviceRepository(), InMemoryUserRepository())
    with pytest.raises(NotFoundError):
        service.register("missing", "android", "Pixel")


def test_messaging_service_generates_events() -> None:
    service = MessagingService()

    message = service.send_message("s1", "u1", "hello")
    event = service.report_audio_event("s1", "u1", "mute")

    assert message.body == "hello"
    assert event.event_type == "mute"
