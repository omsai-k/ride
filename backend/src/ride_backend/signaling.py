from __future__ import annotations

from dataclasses import dataclass

from ride_backend.auth import AuthService
from ride_backend.errors import AuthError
from ride_backend.errors import NotFoundError
from ride_backend.errors import ValidationError
from ride_backend.interfaces import RideSessionRepository


ALLOWED_SIGNALING_TYPES = {
    "join",
    "leave",
    "offer",
    "answer",
    "ice-candidate",
    "mute",
    "unmute",
    "participant-state",
    "heartbeat",
}


@dataclass(frozen=True)
class SignalingEnvelope:
    room_id: str
    user_id: str
    message_type: str
    payload: dict


class SignalingMessageValidator:
    def validate(self, payload: dict) -> SignalingEnvelope:
        for field in ("room_id", "user_id", "type", "payload"):
            if field not in payload:
                raise ValidationError(f"Missing signaling field: {field}")

        room_id = payload["room_id"]
        user_id = payload["user_id"]
        message_type = payload["type"]
        envelope_payload = payload["payload"]

        if not isinstance(room_id, str) or not room_id.strip():
            raise ValidationError("room_id must be a non-empty string")
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValidationError("user_id must be a non-empty string")
        if message_type not in ALLOWED_SIGNALING_TYPES:
            raise ValidationError("Unsupported signaling type")
        if not isinstance(envelope_payload, dict):
            raise ValidationError("payload must be an object")

        return SignalingEnvelope(
            room_id=room_id.strip(),
            user_id=user_id.strip(),
            message_type=message_type,
            payload=envelope_payload,
        )


class RoomMembershipService:
    def __init__(self, session_repo: RideSessionRepository) -> None:
        self._session_repo = session_repo
        self._members: dict[str, set[str]] = {}

    def join(self, room_id: str, user_id: str) -> None:
        session = self._session_repo.get_by_id(room_id)
        if session is None:
            raise NotFoundError("Room does not map to a ride session")
        self._members.setdefault(room_id, set()).add(user_id)

    def leave(self, room_id: str, user_id: str) -> None:
        members = self._members.get(room_id, set())
        members.discard(user_id)

    def ensure_member(self, room_id: str, user_id: str) -> None:
        members = self._members.get(room_id, set())
        if user_id not in members:
            raise AuthError("User is not a room member")

    def list_members(self, room_id: str) -> list[str]:
        return sorted(self._members.get(room_id, set()))


class SignalingGateway:
    def __init__(
        self,
        auth_service: AuthService,
        validator: SignalingMessageValidator,
        membership: RoomMembershipService,
    ) -> None:
        self._auth = auth_service
        self._validator = validator
        self._membership = membership

    def handle(self, token: str, raw_payload: dict) -> SignalingEnvelope:
        claims = self._auth.authorize(token)
        envelope = self._validator.validate(raw_payload)

        token_sub = claims.get("sub")
        if token_sub != envelope.user_id:
            raise AuthError("Token subject mismatch")

        if envelope.message_type == "join":
            self._membership.join(envelope.room_id, envelope.user_id)
            return envelope

        if envelope.message_type == "leave":
            self._membership.leave(envelope.room_id, envelope.user_id)
            return envelope

        self._membership.ensure_member(envelope.room_id, envelope.user_id)
        return envelope
