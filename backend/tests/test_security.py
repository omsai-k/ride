import pytest

from ride_backend.errors import AuthError
from ride_backend.security import RoleAuthorizer


def test_require_role_success() -> None:
    authz = RoleAuthorizer()
    authz.require_role({"role": "admin", "sub": "u1"}, {"admin"})


def test_require_role_failure() -> None:
    authz = RoleAuthorizer()
    with pytest.raises(AuthError):
        authz.require_role({"role": "rider"}, {"admin"})


def test_require_subject_success_and_failure() -> None:
    authz = RoleAuthorizer()
    authz.require_subject({"sub": "u1"}, "u1")
    with pytest.raises(AuthError):
        authz.require_subject({"sub": "u2"}, "u1")
