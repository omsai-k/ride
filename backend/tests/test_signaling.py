import pytest

from ride_backend.auth import AuthService
from ride_backend.auth import PasswordHasher
from ride_backend.auth import TokenService
from ride_backend.config import AppConfig
from ride_backend.errors import AuthError
from ride_backend.errors import NotFoundError
from ride_backend.errors import ValidationError
from ride_backend.models import RideSession
from ride_backend.models import User
from ride_backend.repositories import InMemoryRideSessionRepository
from ride_backend.repositories import InMemoryUserRepository
from ride_backend.signaling import RoomMembershipService
from ride_backend.signaling import SignalingGateway
from ride_backend.signaling import SignalingMessageValidator


def build_gateway() -> tuple[SignalingGateway, str]:
    users = InMemoryUserRepository()
    sessions = InMemoryRideSessionRepository()
    users.save(User(id="u1", email="rider@example.com", display_name="Rider", password_hash=PasswordHasher().hash("secret")))
    sessions.save(RideSession(id="s1", owner_user_id="u1", title="Ride"))

    auth = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))
    token = auth.login("rider@example.com", "secret")
    gateway = SignalingGateway(auth, SignalingMessageValidator(), RoomMembershipService(sessions))
    return gateway, token


def test_validator_rejects_missing_fields() -> None:
    with pytest.raises(ValidationError):
        SignalingMessageValidator().validate({"room_id": "s1"})


def test_gateway_join_and_message_flow() -> None:
    gateway, token = build_gateway()
    joined = gateway.handle(token, {"room_id": "s1", "user_id": "u1", "type": "join", "payload": {}})
    assert joined.message_type == "join"

    sent = gateway.handle(token, {"room_id": "s1", "user_id": "u1", "type": "offer", "payload": {"sdp": "x"}})
    assert sent.message_type == "offer"


def test_gateway_subject_mismatch_fails() -> None:
    gateway, token = build_gateway()
    with pytest.raises(AuthError):
        gateway.handle(token, {"room_id": "s1", "user_id": "u2", "type": "join", "payload": {}})


def test_membership_requires_existing_session() -> None:
    users = InMemoryUserRepository()
    sessions = InMemoryRideSessionRepository()
    users.save(User(id="u1", email="rider@example.com", display_name="Rider", password_hash=PasswordHasher().hash("secret")))
    auth = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))
    token = auth.login("rider@example.com", "secret")
    gateway = SignalingGateway(auth, SignalingMessageValidator(), RoomMembershipService(sessions))

    with pytest.raises(NotFoundError):
        gateway.handle(token, {"room_id": "missing", "user_id": "u1", "type": "join", "payload": {}})
