# Ride Backend

This package now provides a runnable RiderComm backend for mobile clients:

- REST API for auth, user, ride sessions, participants, devices, and events.
- WebSocket signaling endpoint for RTC message flow.
- SOLID-aligned service architecture and test suite.

## Start backend

```bash
python -m pip install -r requirements.txt
python -m uvicorn ride_backend.server:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

Alternative install:

```bash
python -m pip install -e .
```

If you use the editable install above, you can run without `--app-dir src`.

Health check:

```bash
curl http://localhost:8000/health
```

## Run tests

```bash
python -m pytest
```
