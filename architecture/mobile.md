# Mobile App Architecture

## Overview
The mobile app is cross-platform (Android/iOS) and built with a shared codebase (Flutter or React Native), with native modules for audio, Bluetooth, and RTC.

## Layers
1. **Presentation/UI**
   - Ride session list, join/create, voice controls, music status
   - Push-to-talk, open mic, participant management
2. **State Management**
   - Redux/MobX/Provider (Flutter) or Redux/Context (React Native)
   - Handles user/session/device state
3. **Audio/Bluetooth Integration**
   - Native plugins for audio routing, Bluetooth profile switching
   - FFI to C++/Rust DSP modules
4. **RTC Integration**
   - WebRTC native bindings
   - Handles signaling, media, participant state
5. **Networking**
   - REST for CRUD, WebSocket for RTC signaling
   - JWT auth, error handling, reconnection
6. **Background Services**
   - Keep-alive for rides, notifications, reconnection
   - Handle OS background execution limits

## Platform-Specific Notes
- Android: Use AudioManager, Bluetooth APIs, background services
- iOS: Use AVAudioSession, CallKit, background modes

## Extensibility
- Modular for future features (location, ride recording, etc)
