from ride_backend.errors import ValidationError


def require_keys(payload: dict, required: set[str]) -> None:
    missing = required.difference(payload)
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise ValidationError(f"Missing fields: {missing_fields}")


def require_non_empty_string(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string")
    if not value.strip():
        raise ValidationError(f"{field_name} must be non-empty")
    return value.strip()


def validate_email(value: object) -> str:
    email = require_non_empty_string(value, "email")
    if "@" not in email or "." not in email:
        raise ValidationError("email must be valid")
    return email
