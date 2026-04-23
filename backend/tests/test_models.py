from dataclasses import asdict
from datetime import UTC
from datetime import datetime

from ride_backend.models import AudioEvent
from ride_backend.models import Device
from ride_backend.models import Message
from ride_backend.models import Participant
from ride_backend.models import RideSession
from ride_backend.models import RtcSession
from ride_backend.models import User


def test_user_model_roundtrip() -> None:
    user = User(id="u1", email="rider@example.com", display_name="Rider", password_hash="x")
    payload = asdict(user)
    assert payload["id"] == "u1"
    assert payload["role"] == "rider"


def test_all_models_construct() -> None:
    now = datetime.now(UTC)
    device = Device(id="d1", user_id="u1", platform="android", name="Pixel")
    session = RideSession(id="s1", owner_user_id="u1", title="Sunday ride")
    participant = Participant(id="p1", ride_session_id="s1", user_id="u1")
    message = Message(id="m1", ride_session_id="s1", sender_user_id="u1", body="hello", created_at=now)
    audio = AudioEvent(id="a1", ride_session_id="s1", user_id="u1", event_type="mute", created_at=now)
    rtc = RtcSession(id="r1", ride_session_id="s1", room_id="room-1")

    assert device.platform == "android"
    assert session.status == "active"
    assert participant.state == "joined"
    assert message.body == "hello"
    assert audio.event_type == "mute"
    assert rtc.state == "open"
