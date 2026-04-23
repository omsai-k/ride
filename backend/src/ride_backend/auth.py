from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid

from ride_backend.config import AppConfig
from ride_backend.errors import AuthError
from ride_backend.errors import ConflictError
from ride_backend.interfaces import UserRepository
from ride_backend.models import User


class PasswordHasher:
    def hash(self, plaintext: str) -> str:
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        return f"sha256${digest}"

    def verify(self, plaintext: str, digest: str) -> bool:
        return hmac.compare_digest(self.hash(plaintext), digest)


class TokenService:
    def __init__(self, config: AppConfig) -> None:
        self._secret = config.jwt_secret.encode("utf-8")
        self._expiry_seconds = config.jwt_expiry_seconds

    def issue(self, user_id: str, role: str) -> str:
        now = int(time.time())
        payload = {"sub": user_id, "role": role, "iat": now, "exp": now + self._expiry_seconds}
        payload_raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        payload_b64 = base64.urlsafe_b64encode(payload_raw).decode("ascii")
        signature = hmac.new(self._secret, payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
        return f"{payload_b64}.{signature}"

    def verify(self, token: str) -> dict[str, str | int]:
        try:
            payload_b64, signature = token.split(".", maxsplit=1)
        except ValueError as exc:
            raise AuthError("Malformed token") from exc

        expected = hmac.new(self._secret, payload_b64.encode("ascii"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise AuthError("Invalid token signature")

        payload_raw = base64.urlsafe_b64decode(payload_b64.encode("ascii"))
        payload = json.loads(payload_raw.decode("utf-8"))
        if int(payload["exp"]) < int(time.time()):
            raise AuthError("Token expired")
        return payload


class AuthService:
    def __init__(self, user_repo: UserRepository, hasher: PasswordHasher, token_service: TokenService) -> None:
        self._user_repo = user_repo
        self._hasher = hasher
        self._token_service = token_service

    def register(self, email: str, password: str, display_name: str) -> User:
        existing = self._user_repo.get_by_email(email)
        if existing is not None:
            raise ConflictError("Email already exists")

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            display_name=display_name,
            password_hash=self._hasher.hash(password),
        )
        return self._user_repo.save(user)

    def login(self, email: str, password: str) -> str:
        user = self._user_repo.get_by_email(email)
        if user is None:
            raise AuthError("Invalid credentials")
        if not self._hasher.verify(password, user.password_hash):
            raise AuthError("Invalid credentials")
        return self._token_service.issue(user.id, user.role)

    def authorize(self, token: str) -> dict[str, str | int]:
        return self._token_service.verify(token)
