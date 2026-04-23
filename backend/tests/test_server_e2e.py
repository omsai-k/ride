from fastapi.testclient import TestClient

from ride_backend.server import build_app


def test_http_and_websocket_end_to_end() -> None:
    app = build_app()
    client = TestClient(app)

    register = client.post(
        "/auth/register",
        json={
            "email": "rider@example.com",
            "password": "secret123",
            "display_name": "Rider",
        },
    )
    assert register.status_code == 200
    user = register.json()

    login = client.post(
        "/auth/login",
        json={"email": "rider@example.com", "password": "secret123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    create_session = client.post(
        "/ride-sessions",
        json={"owner_user_id": user["id"], "title": "Morning Ride"},
    )
    assert create_session.status_code == 200
    session_id = create_session.json()["id"]

    join = client.post(
        "/participants/join",
        json={"ride_session_id": session_id, "user_id": user["id"]},
    )
    assert join.status_code == 200

    with client.websocket_connect(f"/ws/rtc/{session_id}?token={token}") as ws:
        ws.send_json(
            {
                "user_id": user["id"],
                "type": "join",
                "payload": {},
            },
        )
        ack = ws.receive_json()
        assert ack["type"] == "ack"
        assert ack["message_type"] == "join"
