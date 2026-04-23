# Mobile

Flutter mobile app for Android and iOS.

## Prerequisites

- Flutter SDK installed and available in PATH.
- Android Studio (for Android SDK/emulator).
- Xcode (for iOS simulator/device, macOS only).

## First-time bootstrap

Run in this folder:

```bash
flutter create . --platforms=android,ios
flutter pub get
```

This generates native host folders (`android/` and `ios/`) while keeping the existing app code in `lib/`.

## Run backend first

From `backend/`:

```bash
python -m pip install -e .
python -m uvicorn ride_backend.server:app --host 0.0.0.0 --port 8000 --reload
```

## Run app on Android

```bash
flutter run -d android
```

Android emulator uses `10.0.2.2` to reach host machine `localhost` by default.

## Run app on iOS

On macOS:

```bash
flutter run -d ios
```

iOS simulator defaults to `localhost` automatically.

## Run on physical devices (no source edits)

Use compile-time overrides so you do not need to change app code:

```bash
flutter run -d <device-id> --dart-define=RIDE_API_HOST=192.168.1.20 --dart-define=RIDE_API_PORT=8000
```

- `RIDE_API_HOST`: machine where backend is running (usually your laptop LAN IP)
- `RIDE_API_PORT`: backend port (default `8000`)

The app derives both REST and WebSocket URLs from these values.

## State and session architecture

- Production-style state management via Riverpod (`StateNotifier` + immutable state model)
- Auth session persistence with `SharedPreferences`
- Automatic session restore on app start
- Explicit logout clears persisted session and signaling connection

## Core app flow

1. Register and login from the first screen.
2. Create a ride session.
3. Join a session.
4. App opens signaling WebSocket and sends a `join` message.
