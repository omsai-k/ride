import pytest

from ride_backend.errors import ValidationError
from ride_backend.mobile_flows import AuthFlow
from ride_backend.mobile_flows import AuthFlowState
from ride_backend.mobile_flows import LifecycleCoordinator
from ride_backend.mobile_flows import RideSessionFlow
from ride_backend.mobile_flows import RideSessionFlowState
from ride_backend.mobile_flows import VoiceControlState
from ride_backend.mobile_flows import VoiceControls


def test_auth_flow_login_logout() -> None:
    flow = AuthFlow()
    state = AuthFlowState()
    flow.login_success(state, "token-1")
    assert state.is_authenticated is True
    flow.logout(state)
    assert state.is_authenticated is False


def test_auth_flow_rejects_empty_token() -> None:
    flow = AuthFlow()
    with pytest.raises(ValidationError):
        flow.login_success(AuthFlowState(), " ")


def test_ride_session_flow_and_participants() -> None:
    flow = RideSessionFlow()
    state = RideSessionFlowState()
    flow.enter_session(state, "s1")
    flow.set_participants(state, ["u2", "u1", "u2"])
    assert state.current_session_id == "s1"
    assert state.participants == ["u1", "u2"]


def test_voice_controls_modes() -> None:
    controls = VoiceControls()
    state = VoiceControlState()
    controls.set_mode(state, "open-mic")
    assert state.mode == "open-mic"
    with pytest.raises(ValidationError):
        controls.set_mode(state, "invalid")


def test_lifecycle_coordinator() -> None:
    lifecycle = LifecycleCoordinator()
    assert lifecycle.on_background()["should_reduce_network"] is True
    assert lifecycle.on_foreground()["should_reconnect_realtime"] is True
