from __future__ import annotations

from dataclasses import asdict

from ride_backend.auth import AuthService
from ride_backend.services import DeviceService
from ride_backend.services import MessagingService
from ride_backend.services import ParticipantService
from ride_backend.services import RideSessionService
from ride_backend.services import UserService
from ride_backend.validation import require_keys
from ride_backend.validation import require_non_empty_string
from ride_backend.validation import validate_email


class ApiHandlers:
    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        ride_session_service: RideSessionService,
        participant_service: ParticipantService,
        device_service: DeviceService,
        messaging_service: MessagingService,
    ) -> None:
        self._auth = auth_service
        self._users = user_service
        self._sessions = ride_session_service
        self._participants = participant_service
        self._devices = device_service
        self._messages = messaging_service

    def register(self, payload: dict) -> dict:
        require_keys(payload, {"email", "password", "display_name"})
        user = self._auth.register(
            email=validate_email(payload["email"]),
            password=require_non_empty_string(payload["password"], "password"),
            display_name=require_non_empty_string(payload["display_name"], "display_name"),
        )
        return asdict(user)

    def login(self, payload: dict) -> dict:
        require_keys(payload, {"email", "password"})
        token = self._auth.login(
            email=validate_email(payload["email"]),
            password=require_non_empty_string(payload["password"], "password"),
        )
        return {"access_token": token, "token_type": "Bearer"}

    def get_user_me(self, user_id: str) -> dict:
        return asdict(self._users.get_me(user_id))

    def patch_user_me(self, user_id: str, payload: dict) -> dict:
        require_keys(payload, {"display_name"})
        updated = self._users.update_me(user_id, require_non_empty_string(payload["display_name"], "display_name"))
        return asdict(updated)

    def create_ride_session(self, payload: dict) -> dict:
        require_keys(payload, {"owner_user_id", "title"})
        session = self._sessions.create(
            owner_user_id=require_non_empty_string(payload["owner_user_id"], "owner_user_id"),
            title=require_non_empty_string(payload["title"], "title"),
        )
        return asdict(session)

    def list_ride_sessions(self) -> list[dict]:
        return [asdict(session) for session in self._sessions.list_all()]

    def patch_ride_session(self, session_id: str, payload: dict) -> dict:
        require_keys(payload, {"title", "status"})
        updated = self._sessions.update(
            session_id,
            title=require_non_empty_string(payload["title"], "title"),
            status=require_non_empty_string(payload["status"], "status"),
        )
        return asdict(updated)

    def join_participant(self, payload: dict) -> dict:
        require_keys(payload, {"ride_session_id", "user_id"})
        participant = self._participants.join(
            ride_session_id=require_non_empty_string(payload["ride_session_id"], "ride_session_id"),
            user_id=require_non_empty_string(payload["user_id"], "user_id"),
        )
        return asdict(participant)

    def leave_participant(self, payload: dict) -> dict:
        require_keys(payload, {"ride_session_id", "user_id"})
        participant = self._participants.leave(
            ride_session_id=require_non_empty_string(payload["ride_session_id"], "ride_session_id"),
            user_id=require_non_empty_string(payload["user_id"], "user_id"),
        )
        return asdict(participant)

    def list_participants(self, ride_session_id: str) -> list[dict]:
        participants = self._participants.list_participants(ride_session_id)
        return [asdict(participant) for participant in participants]

    def register_device(self, payload: dict) -> dict:
        require_keys(payload, {"user_id", "platform", "name"})
        device = self._devices.register(
            user_id=require_non_empty_string(payload["user_id"], "user_id"),
            platform=require_non_empty_string(payload["platform"], "platform"),
            name=require_non_empty_string(payload["name"], "name"),
        )
        return asdict(device)

    def list_devices(self, user_id: str) -> list[dict]:
        return [asdict(device) for device in self._devices.list_for_user(user_id)]

    def post_message(self, payload: dict) -> dict:
        require_keys(payload, {"ride_session_id", "sender_user_id", "body"})
        message = self._messages.send_message(
            ride_session_id=require_non_empty_string(payload["ride_session_id"], "ride_session_id"),
            sender_user_id=require_non_empty_string(payload["sender_user_id"], "sender_user_id"),
            body=require_non_empty_string(payload["body"], "body"),
        )
        return asdict(message)

    def report_audio_event(self, payload: dict) -> dict:
        require_keys(payload, {"ride_session_id", "user_id", "event_type"})
        event = self._messages.report_audio_event(
            ride_session_id=require_non_empty_string(payload["ride_session_id"], "ride_session_id"),
            user_id=require_non_empty_string(payload["user_id"], "user_id"),
            event_type=require_non_empty_string(payload["event_type"], "event_type"),
        )
        return asdict(event)
