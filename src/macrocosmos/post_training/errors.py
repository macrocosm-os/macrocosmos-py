"""Errors, named like Tinker's so `except tinker.NotFoundError` ports unchanged."""

from __future__ import annotations

from typing import Any, Optional

from macrocosmos.types._exceptions import MacrocosmosError


class PostTrainingError(MacrocosmosError):
    """Base class for every error raised by `macrocosmos.post_training`."""


class APIConnectionError(PostTrainingError):
    """The gateway could not be reached."""


class APITimeoutError(PostTrainingError, TimeoutError):
    """A future did not resolve within its timeout."""


class APIStatusError(PostTrainingError):
    """The gateway answered with an error status."""

    status_code: int = 0

    def __init__(self, message: str, *, status_code: int, body: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class BadRequestError(APIStatusError):
    status_code = 400


class AuthenticationError(APIStatusError):
    status_code = 401


class PermissionDeniedError(APIStatusError):
    status_code = 403


class NotFoundError(APIStatusError):
    status_code = 404


class ConflictError(APIStatusError):
    """The session is closed, or its model failed to build."""

    status_code = 409


class PayloadTooLargeError(APIStatusError):
    """A request body was over the gateway's size limit."""

    status_code = 413


class UnprocessableEntityError(APIStatusError):
    status_code = 422


class RateLimitError(APIStatusError):
    status_code = 429


class InternalServerError(APIStatusError):
    status_code = 500


class NotSupportedError(PostTrainingError, NotImplementedError):
    """A Tinker feature Macrocosmos doesn't offer yet."""


class RequestFailedError(PostTrainingError):
    """A queued job (training op or sampling request) finished in failure."""

    def __init__(self, message: str, *, handle: Optional[str] = None) -> None:
        super().__init__(message)
        self.handle = handle


_BY_STATUS = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    413: PayloadTooLargeError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def error_for_status(status: int, message: str, body: Any = None) -> APIStatusError:
    cls = _BY_STATUS.get(status) or (
        InternalServerError if status >= 500 else APIStatusError
    )
    return cls(message, status_code=status, body=body)
