class ValidationError(ValueError):
    """Raised when incoming payloads are invalid."""


class AuthError(ValueError):
    """Raised when authentication or authorization fails."""


class NotFoundError(LookupError):
    """Raised when a requested resource is not found."""


class ConflictError(RuntimeError):
    """Raised when a write operation conflicts with existing state."""
