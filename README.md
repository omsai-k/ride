# ride
RiderComm is a mobile-first voice communication app for riders, with a Flutter client (iOS and Android) and a Python backend (REST + WebSocket signaling).

## Prerequisites

- Python 3.11+
- Flutter SDK
- Android Studio (Android emulator/device)
- Xcode (for iOS simulator/device on macOS)

## End-to-end run guide

### 1. Start backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn ride_backend.server:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

Alternative backend install (editable package mode):

```bash
cd backend
python -m pip install -e .
```

### 2. Bootstrap Flutter project (first time only)

```bash
cd mobile
flutter create . --platforms=android,ios
flutter pub get
```

### 3. Run mobile app

Android:

```bash
flutter run -d android
```

iOS (macOS only):

```bash
flutter run -d ios
```

Physical device (Android or iOS) without editing source:

```bash
flutter run -d <device-id> --dart-define=RIDE_API_HOST=192.168.1.20 --dart-define=RIDE_API_PORT=8000
```

## Validation

Backend tests:

```bash
cd backend
python -m pytest
```
