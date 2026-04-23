from __future__ import annotations

from dataclasses import dataclass

from ride_backend.errors import ValidationError


A2DP = "a2dp"
HFP = "hfp"


@dataclass
class BluetoothState:
    active_profile: str = A2DP
    supported_profiles: set[str] | None = None

    def __post_init__(self) -> None:
        if self.supported_profiles is None:
            self.supported_profiles = {A2DP, HFP}


class BluetoothProfileManager:
    def switch_for_voice(self, state: BluetoothState, voice_active: bool) -> BluetoothState:
        if voice_active:
            if HFP in state.supported_profiles:
                state.active_profile = HFP
            else:
                state.active_profile = A2DP
            return state

        if A2DP in state.supported_profiles:
            state.active_profile = A2DP
            return state

        raise ValidationError("No valid profile available")


@dataclass
class MixInstruction:
    music_gain: float
    voice_gain: float


class AudioMixer:
    def compute_mix(self, voice_active: bool) -> MixInstruction:
        if voice_active:
            return MixInstruction(music_gain=0.35, voice_gain=1.0)
        return MixInstruction(music_gain=1.0, voice_gain=0.0)
