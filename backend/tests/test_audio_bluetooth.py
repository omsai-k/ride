import pytest

from ride_backend.audio_bluetooth import A2DP
from ride_backend.audio_bluetooth import BluetoothProfileManager
from ride_backend.audio_bluetooth import BluetoothState
from ride_backend.audio_bluetooth import HFP
from ride_backend.audio_bluetooth import AudioMixer
from ride_backend.errors import ValidationError


def test_switch_for_voice_and_back() -> None:
    manager = BluetoothProfileManager()
    state = BluetoothState()

    manager.switch_for_voice(state, True)
    assert state.active_profile == HFP

    manager.switch_for_voice(state, False)
    assert state.active_profile == A2DP


def test_switch_fallback_and_failure() -> None:
    manager = BluetoothProfileManager()
    fallback = BluetoothState(active_profile=A2DP, supported_profiles={A2DP})
    manager.switch_for_voice(fallback, True)
    assert fallback.active_profile == A2DP

    invalid = BluetoothState(active_profile=HFP, supported_profiles={HFP})
    with pytest.raises(ValidationError):
        manager.switch_for_voice(invalid, False)


def test_audio_mixer_ducking() -> None:
    mixer = AudioMixer()
    voice = mixer.compute_mix(True)
    quiet = mixer.compute_mix(False)

    assert voice.music_gain < 1.0
    assert voice.voice_gain == 1.0
    assert quiet.music_gain == 1.0
    assert quiet.voice_gain == 0.0
