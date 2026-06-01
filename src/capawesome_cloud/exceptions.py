"""Exception hierarchy for the Capawesome Cloud SDK.

All errors raised by the SDK derive from :class:`CapawesomeCloudError`, so a single
``except CapawesomeCloudError`` will catch everything the SDK can raise.
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

__all__ = [
    "CapawesomeCloudError",
    "APIConnectionError",
    "APITimeoutError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]


class CapawesomeCloudError(Exception):
    """Base class for every error raised by the SDK."""


class APIConnectionError(CapawesomeCloudError):
    """Raised when the request could not reach the API (network failure)."""

    def __init__(
        self,
        message: str = "Could not connect to the Capawesome Cloud API.",
        *,
        request: Optional[httpx.Request] = None,
    ) -> None:
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    """Raised when the request timed out."""

    def __init__(self, *, request: Optional[httpx.Request] = None) -> None:
        super().__init__("Request to the Capawesome Cloud API timed out.", request=request)


class APIStatusError(CapawesomeCloudError):
    """Raised when the API returns a non-success HTTP status code.

    The ``message`` is taken from the API response body (``{"message": ...}``)
    when available, otherwise the HTTP reason phrase is used.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        response: httpx.Response,
        body: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
        self.body = body


class BadRequestError(APIStatusError):
    """HTTP 400."""


class AuthenticationError(APIStatusError):
    """HTTP 401 - missing or invalid API token."""


class PermissionDeniedError(APIStatusError):
    """HTTP 403."""


class NotFoundError(APIStatusError):
    """HTTP 404."""


class ConflictError(APIStatusError):
    """HTTP 409."""


class UnprocessableEntityError(APIStatusError):
    """HTTP 422 - request validation failed."""


class RateLimitError(APIStatusError):
    """HTTP 429 - too many requests."""


class InternalServerError(APIStatusError):
    """HTTP 5xx."""


_STATUS_EXCEPTIONS: dict[int, type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def exception_from_response(response: httpx.Response) -> APIStatusError:
    """Build the most specific :class:`APIStatusError` for an HTTP response."""
    status = response.status_code
    body: Optional[Any] = None
    message: Optional[str] = None
    try:
        body = response.json()
        if isinstance(body, dict):
            raw = body.get("message")
            if isinstance(raw, str):
                message = raw
    except ValueError:
        body = response.text or None

    if not message:
        message = f"HTTP {status} {response.reason_phrase}".strip()

    exc_class = _STATUS_EXCEPTIONS.get(status)
    if exc_class is None:
        exc_class = InternalServerError if status >= 500 else APIStatusError
    return exc_class(message, status_code=status, response=response, body=body)
