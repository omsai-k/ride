import pytest

from ride_backend.auth import AuthService
from ride_backend.auth import PasswordHasher
from ride_backend.auth import TokenService
from ride_backend.config import AppConfig
from ride_backend.errors import AuthError
from ride_backend.errors import ConflictError
from ride_backend.models import User
from ride_backend.repositories import InMemoryUserRepository


def test_password_hasher_roundtrip() -> None:
    hasher = PasswordHasher()
    digest = hasher.hash("secret")
    assert digest.startswith("sha256$")
    assert hasher.verify("secret", digest)
    assert not hasher.verify("wrong", digest)


def test_token_service_issue_and_verify() -> None:
    tokens = TokenService(AppConfig(jwt_secret="test-secret", jwt_expiry_seconds=120))
    token = tokens.issue(user_id="u1", role="rider")

    payload = tokens.verify(token)
    assert payload["sub"] == "u1"
    assert payload["role"] == "rider"


def test_token_service_rejects_bad_signature() -> None:
    tokens = TokenService(AppConfig(jwt_secret="test-secret", jwt_expiry_seconds=120))
    token = tokens.issue(user_id="u1", role="rider") + "tamper"
    with pytest.raises(AuthError):
        tokens.verify(token)


def test_auth_service_register_and_login() -> None:
    users = InMemoryUserRepository()
    service = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))

    user = service.register("rider@example.com", "secret", "Rider")
    token = service.login("rider@example.com", "secret")

    assert user.email == "rider@example.com"
    assert isinstance(token, str)
    assert service.authorize(token)["sub"] == user.id


def test_auth_service_rejects_duplicate_email() -> None:
    users = InMemoryUserRepository()
    service = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))
    users.save(User(id="u1", email="rider@example.com", display_name="R", password_hash="h"))

    with pytest.raises(ConflictError):
        service.register("rider@example.com", "secret", "Another")


def test_auth_service_rejects_bad_login() -> None:
    users = InMemoryUserRepository()
    users.save(User(id="u1", email="rider@example.com", display_name="R", password_hash=PasswordHasher().hash("secret")))
    service = AuthService(users, PasswordHasher(), TokenService(AppConfig.default()))

    with pytest.raises(AuthError):
        service.login("rider@example.com", "wrong")
