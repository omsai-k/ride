from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi import Query
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.responses import JSONResponse

from ride_backend.api import ApiHandlers
from ride_backend.auth import AuthService
from ride_backend.auth import PasswordHasher
from ride_backend.auth import TokenService
from ride_backend.config import AppConfig
from ride_backend.errors import AuthError
from ride_backend.errors import ConflictError
from ride_backend.errors import NotFoundError
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
from ride_backend.signaling import RoomMembershipService
from ride_backend.signaling import SignalingGateway
from ride_backend.signaling import SignalingMessageValidator


def build_app() -> FastAPI:
    users = InMemoryUserRepository()
    devices = InMemoryDeviceRepository()
    sessions = InMemoryRideSessionRepository()
    participants = InMemoryParticipantRepository()

    auth_service = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))
    api = ApiHandlers(
        auth_service=auth_service,
        user_service=UserService(users),
        ride_session_service=RideSessionService(sessions),
        participant_service=ParticipantService(participants, sessions),
        device_service=DeviceService(devices, users),
        messaging_service=MessagingService(),
    )
    signaling = SignalingGateway(
        auth_service=auth_service,
        validator=SignalingMessageValidator(),
        membership=RoomMembershipService(sessions),
    )

    app = FastAPI(title="RiderComm Backend", version="0.2.0")

    @app.exception_handler(ValidationError)
    async def validation_handler(_, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"error": str(exc)})

    @app.exception_handler(AuthError)
    async def auth_handler(_, exc: AuthError) -> JSONResponse:
        return JSONResponse(status_code=401, content={"error": str(exc)})

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(ConflictError)
    async def conflict_handler(_, exc: ConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"error": str(exc)})

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/auth/register")
    async def register(payload: dict) -> dict:
        return api.register(payload)

    @app.post("/auth/login")
    async def login(payload: dict) -> dict:
        return api.login(payload)

    @app.get("/user/me/{user_id}")
    async def me(user_id: str) -> dict:
        return api.get_user_me(user_id)

    @app.patch("/user/me/{user_id}")
    async def patch_me(user_id: str, payload: dict) -> dict:
        return api.patch_user_me(user_id, payload)

    @app.post("/ride-sessions")
    async def create_ride_session(payload: dict) -> dict:
        return api.create_ride_session(payload)

    @app.get("/ride-sessions")
    async def list_ride_sessions() -> list[dict]:
        return api.list_ride_sessions()

    @app.patch("/ride-sessions/{session_id}")
    async def patch_ride_session(session_id: str, payload: dict) -> dict:
        return api.patch_ride_session(session_id, payload)

    @app.post("/participants/join")
    async def join_participant(payload: dict) -> dict:
        return api.join_participant(payload)

    @app.post("/participants/leave")
    async def leave_participant(payload: dict) -> dict:
        return api.leave_participant(payload)

    @app.get("/participants/{ride_session_id}")
    async def list_participants(ride_session_id: str) -> list[dict]:
        return api.list_participants(ride_session_id)

    @app.post("/device/register")
    async def register_device(payload: dict) -> dict:
        return api.register_device(payload)

    @app.get("/device/{user_id}")
    async def list_devices(user_id: str) -> list[dict]:
        return api.list_devices(user_id)

    @app.post("/messages")
    async def post_message(payload: dict) -> dict:
        return api.post_message(payload)

    @app.post("/audio-events")
    async def post_audio_event(payload: dict) -> dict:
        return api.report_audio_event(payload)

    @app.websocket("/ws/rtc/{room_id}")
    async def rtc_socket(websocket: WebSocket, room_id: str, token: str = Query(default="")) -> None:
        await websocket.accept()
        if not token:
            await websocket.send_json({"type": "error", "error": "Missing token"})
            await websocket.close()
            return

        try:
            while True:
                raw_text = await websocket.receive_text()
                payload = json.loads(raw_text)
                payload["room_id"] = room_id
                envelope = signaling.handle(token, payload)
                await websocket.send_json(
                    {
                        "type": "ack",
                        "room_id": envelope.room_id,
                        "user_id": envelope.user_id,
                        "message_type": envelope.message_type,
                    },
                )
        except WebSocketDisconnect:
            return

    return app


app = build_app()
