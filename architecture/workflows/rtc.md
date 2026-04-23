# RTC Workflow

## Purpose
Implement the real-time communication infrastructure that connects riders in low-latency voice sessions.

## Scope
- WebRTC peer connection management
- Signaling flow via WebSocket
- ICE candidate exchange
- Media encryption and session state
- Optional SFU architecture for group calls

## Inputs
- `architecture/rtc.md`
- `architecture/api.md`
- `architecture/backend.md`
- `architecture/mobile.md`

## Workflow Steps
1. Define signaling message schema: join, leave, offer, answer, ice-candidate, mute, unmute.
2. Implement RTC room lifecycle on the backend.
3. Implement client-side signaling adapter in mobile app.
4. Create WebRTC peer connection setup and teardown.
5. Handle ICE candidate gathering and exchange.
6. Add participant state updates and mute/unmute signaling.
7. Add DTLS-SRTP encryption enforcement.
8. Test peer-to-peer RTC for 2 participants.
9. If needed, design and implement SFU relay server for group calls.

## Deliverables
- RTC signaling protocol definition.
- Backend signaling server that supports room join/leave and ICE.
- Client-side WebRTC connection manager.
- End-to-end voice call proof of concept.

## Validation
- Two clients can connect and exchange audio.
- Signaling traffic is authenticated and encrypted.
- The app handles network reconnects and room rejoin.

## Handoff
- Provide call state events to mobile UI.
- Share required native audio routing hooks with Audio workflow.
