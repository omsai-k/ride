from __future__ import annotations

from dataclasses import dataclass

from ride_backend.errors import ValidationError


@dataclass
class AuthFlowState:
    is_authenticated: bool = False
    access_token: str | None = None


class AuthFlow:
    def login_success(self, state: AuthFlowState, access_token: str) -> AuthFlowState:
        if not access_token.strip():
            raise ValidationError("access_token must be non-empty")
        state.is_authenticated = True
        state.access_token = access_token
        return state

    def logout(self, state: AuthFlowState) -> AuthFlowState:
        state.is_authenticated = False
        state.access_token = None
        return state


@dataclass
class RideSessionFlowState:
    current_session_id: str | None = None
    participants: list[str] | None = None

    def __post_init__(self) -> None:
        if self.participants is None:
            self.participants = []


class RideSessionFlow:
    def enter_session(self, state: RideSessionFlowState, session_id: str) -> RideSessionFlowState:
        if not session_id.strip():
            raise ValidationError("session_id must be non-empty")
        state.current_session_id = session_id
        return state

    def set_participants(self, state: RideSessionFlowState, participants: list[str]) -> RideSessionFlowState:
        state.participants = sorted(set(participants))
        return state


@dataclass
class VoiceControlState:
    mode: str = "mute"


class VoiceControls:
    ALLOWED_MODES = {"push-to-talk", "open-mic", "mute"}

    def set_mode(self, state: VoiceControlState, mode: str) -> VoiceControlState:
        if mode not in self.ALLOWED_MODES:
            raise ValidationError("Unsupported voice control mode")
        state.mode = mode
        return state


class LifecycleCoordinator:
    def on_background(self) -> dict[str, bool]:
        return {"should_reduce_network": True, "should_pause_realtime": False}

    def on_foreground(self) -> dict[str, bool]:
        return {"should_reconnect_realtime": True, "should_refresh_state": True}
