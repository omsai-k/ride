import pytest

from ride_backend.errors import ValidationError
from ride_backend.validation import require_keys
from ride_backend.validation import require_non_empty_string
from ride_backend.validation import validate_email


def test_require_keys_passes() -> None:
    payload = {"a": 1, "b": 2}
    require_keys(payload, {"a", "b"})


def test_require_keys_raises_on_missing() -> None:
    with pytest.raises(ValidationError, match="Missing fields"):
        require_keys({"a": 1}, {"a", "b"})


def test_require_non_empty_string() -> None:
    assert require_non_empty_string("  hi  ", "name") == "hi"


@pytest.mark.parametrize("value", [None, 1, "", "  "])
def test_require_non_empty_string_fails(value: object) -> None:
    with pytest.raises(ValidationError):
        require_non_empty_string(value, "name")


def test_validate_email_success() -> None:
    assert validate_email("rider@example.com") == "rider@example.com"


def test_validate_email_invalid() -> None:
    with pytest.raises(ValidationError, match="email must be valid"):
        validate_email("invalid-email")
