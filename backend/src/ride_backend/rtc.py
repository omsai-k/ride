from __future__ import annotations

from dataclasses import dataclass

from ride_backend.errors import NotFoundError
from ride_backend.errors import ValidationError


@dataclass
class PeerConnectionState:
    room_id: str
    user_id: str
    state: str = "connecting"
    offer: str | None = None
    answer: str | None = None
    ice_candidates: list[str] | None = None

    def __post_init__(self) -> None:
        if self.ice_candidates is None:
            self.ice_candidates = []


class RTCSessionManager:
    def __init__(self) -> None:
        self._peers: dict[str, PeerConnectionState] = {}

    @staticmethod
    def _key(room_id: str, user_id: str) -> str:
        return f"{room_id}:{user_id}"

    def create_peer(self, room_id: str, user_id: str) -> PeerConnectionState:
        peer = PeerConnectionState(room_id=room_id, user_id=user_id)
        self._peers[self._key(room_id, user_id)] = peer
        return peer

    def set_offer(self, room_id: str, user_id: str, sdp_offer: str) -> PeerConnectionState:
        peer = self._get(room_id, user_id)
        if not sdp_offer.strip():
            raise ValidationError("Offer must be non-empty")
        peer.offer = sdp_offer
        peer.state = "connecting"
        return peer

    def set_answer(self, room_id: str, user_id: str, sdp_answer: str) -> PeerConnectionState:
        peer = self._get(room_id, user_id)
        if not peer.offer:
            raise ValidationError("Cannot answer before offer")
        if not sdp_answer.strip():
            raise ValidationError("Answer must be non-empty")
        peer.answer = sdp_answer
        peer.state = "connected"
        return peer

    def add_ice_candidate(self, room_id: str, user_id: str, candidate: str) -> PeerConnectionState:
        peer = self._get(room_id, user_id)
        if not candidate.strip():
            raise ValidationError("ICE candidate must be non-empty")
        peer.ice_candidates.append(candidate)
        return peer

    def disconnect(self, room_id: str, user_id: str) -> PeerConnectionState:
        peer = self._get(room_id, user_id)
        peer.state = "disconnected"
        return peer

    def get(self, room_id: str, user_id: str) -> PeerConnectionState:
        return self._get(room_id, user_id)

    def _get(self, room_id: str, user_id: str) -> PeerConnectionState:
        key = self._key(room_id, user_id)
        peer = self._peers.get(key)
        if peer is None:
            raise NotFoundError("Peer session not found")
        return peer
