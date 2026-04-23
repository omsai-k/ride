from ride_backend.api import ApiHandlers
from ride_backend.auth import AuthService
from ride_backend.auth import PasswordHasher
from ride_backend.auth import TokenService
from ride_backend.config import AppConfig
from ride_backend.errors import ValidationError
from ride_backend.repositories import InMemoryDeviceRepository
from ride_backend.repositories import InMemoryParticipantRepository
from ride_backend.repositories import InMemoryRideSessionRepository
from ride_backend.repositories import InMemoryUserRepository
from ride_backend.services import DeviceService
from ride_backend.services import MessagingService
from ride_backend.services import ParticipantService
from ride_backend.services import RideSessionService
from ride_backend.services import UserService


def build_api() -> ApiHandlers:
    users = InMemoryUserRepository()
    sessions = InMemoryRideSessionRepository()
    participants = InMemoryParticipantRepository()
    devices = InMemoryDeviceRepository()

    auth = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))
    user_service = UserService(users)
    session_service = RideSessionService(sessions)
    participant_service = ParticipantService(participants, sessions)
    device_service = DeviceService(devices, users)
    messaging_service = MessagingService()

    return ApiHandlers(auth, user_service, session_service, participant_service, device_service, messaging_service)


def test_auth_and_user_endpoints() -> None:
    api = build_api()

    created = api.register({"email": "rider@example.com", "password": "secret", "display_name": "Rider"})
    login = api.login({"email": "rider@example.com", "password": "secret"})
    me = api.get_user_me(created["id"])
    updated = api.patch_user_me(created["id"], {"display_name": "Captain"})

    assert created["email"] == "rider@example.com"
    assert "access_token" in login
    assert me["id"] == created["id"]
    assert updated["display_name"] == "Captain"


def test_ride_session_and_participant_endpoints() -> None:
    api = build_api()
    owner = api.register({"email": "owner@example.com", "password": "secret", "display_name": "Owner"})
    friend = api.register({"email": "friend@example.com", "password": "secret", "display_name": "Friend"})

    created = api.create_ride_session({"owner_user_id": owner["id"], "title": "Sunset Ride"})
    sessions = api.list_ride_sessions()
    patched = api.patch_ride_session(created["id"], {"title": "Night Ride", "status": "active"})
    joined = api.join_participant({"ride_session_id": created["id"], "user_id": friend["id"]})
    listed = api.list_participants(created["id"])
    left = api.leave_participant({"ride_session_id": created["id"], "user_id": friend["id"]})

    assert sessions[0]["id"] == created["id"]
    assert patched["title"] == "Night Ride"
    assert joined["state"] == "joined"
    assert listed[0]["user_id"] == friend["id"]
    assert left["state"] == "left"


def test_device_message_and_audio_event_endpoints() -> None:
    api = build_api()
    user = api.register({"email": "rider@example.com", "password": "secret", "display_name": "Rider"})
    session = api.create_ride_session({"owner_user_id": user["id"], "title": "Road"})

    device = api.register_device({"user_id": user["id"], "platform": "android", "name": "Pixel"})
    devices = api.list_devices(user["id"])
    message = api.post_message({"ride_session_id": session["id"], "sender_user_id": user["id"], "body": "hello"})
    audio = api.report_audio_event({"ride_session_id": session["id"], "user_id": user["id"], "event_type": "mute"})

    assert device["platform"] == "android"
    assert devices[0]["name"] == "Pixel"
    assert message["body"] == "hello"
    assert audio["event_type"] == "mute"


def test_endpoint_validation() -> None:
    api = build_api()
    try:
        api.register({"email": "rider@example.com", "password": "secret"})
        raise AssertionError("expected ValidationError")
    except ValidationError:
        pass
