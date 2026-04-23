# Mobile App Workflow

## Purpose
Develop the cross-platform RiderComm mobile application with UI, state management, native audio/Bluetooth integration, and RTC glue.

## Scope
- Shared app shell (Flutter or React Native)
- Authentication screens
- Ride session creation/join flow
- Voice controls (push-to-talk, mute/unmute)
- Background execution support
- Native plugin integration for audio, Bluetooth, and WebRTC

## Inputs
- `architecture/mobile.md`
- `architecture/api.md`
- `architecture/rtc.md`
- `architecture/bluetooth.md`
- `architecture/audio-pipeline.md`

## Workflow Steps
1. Initialize the mobile project.
2. Implement authentication and user session handling.
3. Build ride session UI and participant list.
4. Add voice control UI components.
5. Implement state management for user, session, device, and RTC state.
6. Create REST client modules for auth, ride sessions, devices, and messages.
7. Integrate WebSocket signaling for RTC.
8. Add native modules or FFI bindings for audio routing and Bluetooth profile control.
9. Implement background mode and reconnection behavior.
10. Add debug screens for Bluetooth profile status and audio routing.

## Deliverables
- Completed mobile app scaffold with the main flows.
- Auth + ride session CRUD.
- Basic WebRTC join/leave flow.
- Native plugin skeletons for audio and Bluetooth.
- Example run instructions.

## Validation
- Can register/login and view a ride session list.
- Can join a ride session and establish a signaling connection.
- UI reflects mute/open mic state.
- App can recover from background/foreground transitions.

## Handoff
- Pass native audio/Bluetooth integration details to the Bluetooth and Audio workflows.
- Share REST client contracts with the backend workflow.
