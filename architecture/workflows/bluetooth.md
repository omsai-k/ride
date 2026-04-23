# Bluetooth Workflow

## Purpose
Build the Bluetooth management layer that detects helmet profiles and switches audio routing intelligently.

## Scope
- Bluetooth profile detection
- Smart A2DP/HFP switching logic
- Native OS integration
- User-facing status reporting
- Fallback behavior

## Inputs
- `architecture/bluetooth.md`
- `architecture/mobile.md`
- `architecture/audio-pipeline.md`

## Workflow Steps
1. Define supported helmet profiles and device capabilities.
2. Implement detection of connected Bluetooth audio devices.
3. Create profile switch logic based on voice activity and user state.
4. Integrate with mobile audio session management.
5. Add status reporting to the UI.
6. Implement graceful fallback when only one profile is available.
7. Add logs for every profile switch event.
8. Test with representative helmet devices.

## Deliverables
- Native Bluetooth profile manager.
- Profile switch policy implementation.
- Device capability detection module.
- UI status/shadow state for Bluetooth session.

## Validation
- App detects helmet connection and supports A2DP/HFP switching.
- Profile state updates correctly during voice start/end.
- Fallback path works when dual-profile support is unavailable.

## Handoff
- Provide Bluetooth state API to mobile app.
- Provide profile switch triggers to audio workflow.
