import pytest

from ride_backend.config import AppConfig
from ride_backend.errors import AuthError
from ride_backend.errors import ConflictError
from ride_backend.errors import NotFoundError
from ride_backend.errors import ValidationError


def test_default_config_values() -> None:
    cfg = AppConfig.default()
    assert cfg.jwt_secret == "dev-secret"
    assert cfg.jwt_expiry_seconds == 3600


def test_error_types_are_specific() -> None:
    assert issubclass(ValidationError, ValueError)
    assert issubclass(AuthError, ValueError)
    assert issubclass(NotFoundError, LookupError)
    assert issubclass(ConflictError, RuntimeError)


@pytest.mark.parametrize(
    "error_cls",
    [ValidationError, AuthError, NotFoundError, ConflictError],
)
def test_error_classes_raise(error_cls: type[Exception]) -> None:
    with pytest.raises(error_cls):
        raise error_cls("boom")
