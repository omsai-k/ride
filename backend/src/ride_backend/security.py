from __future__ import annotations

from ride_backend.errors import AuthError


class RoleAuthorizer:
    def require_role(self, claims: dict[str, str | int], allowed_roles: set[str]) -> None:
        role = claims.get("role")
        if not isinstance(role, str):
            raise AuthError("Missing role in claims")
        if role not in allowed_roles:
            raise AuthError("Insufficient role")

    def require_subject(self, claims: dict[str, str | int], user_id: str) -> None:
        subject = claims.get("sub")
        if not isinstance(subject, str):
            raise AuthError("Missing subject in claims")
        if subject != user_id:
            raise AuthError("Subject mismatch")
