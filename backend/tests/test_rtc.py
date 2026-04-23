import pytest

from ride_backend.errors import NotFoundError
from ride_backend.errors import ValidationError
from ride_backend.rtc import RTCSessionManager


def test_rtc_offer_answer_candidate_flow() -> None:
    rtc = RTCSessionManager()
    rtc.create_peer("s1", "u1")
    rtc.set_offer("s1", "u1", "offer-sdp")
    rtc.set_answer("s1", "u1", "answer-sdp")
    rtc.add_ice_candidate("s1", "u1", "candidate-1")

    peer = rtc.get("s1", "u1")
    assert peer.state == "connected"
    assert peer.ice_candidates == ["candidate-1"]


def test_rtc_answer_without_offer_fails() -> None:
    rtc = RTCSessionManager()
    rtc.create_peer("s1", "u1")
    with pytest.raises(ValidationError):
        rtc.set_answer("s1", "u1", "answer-sdp")


def test_rtc_missing_peer_fails() -> None:
    rtc = RTCSessionManager()
    with pytest.raises(NotFoundError):
        rtc.get("s1", "u1")
