"""Errors raised by the SDK.

Every error derives from :class:`CapawesomeCloudError`, so a single
``except CapawesomeCloudError`` catches everything the SDK can raise. HTTP
errors (non-2xx responses) are raised as ``CapawesomeCloudError`` directly and
carry ``status`` / ``status_text`` / ``message`` / ``body``. Network failures
raise :class:`APIConnectionError` / :class:`APITimeoutError`.
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

__all__ = [
    "CapawesomeCloudError",
    "APIConnectionError",
    "APITimeoutError",
]


class CapawesomeCloudError(Exception):
    """Base error, and the error raised for non-2xx API responses.

    For HTTP errors, ``status``, ``status_text``, ``response`` and ``body`` are
    populated. For non-HTTP errors (e.g. connection failures or configuration
    problems) ``status`` is ``None``.
    """

    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        status_text: Optional[str] = None,
        response: Optional[httpx.Response] = None,
        body: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.status_text = status_text
        self.response = response
        self.body = body


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


def exception_from_response(response: httpx.Response) -> CapawesomeCloudError:
    """Build a :class:`CapawesomeCloudError` for a non-2xx HTTP response."""
    status = response.status_code
    body: Optional[Any] = None
    message: Optional[str] = None
    try:
        body = response.json()
        message = _message_from_body(body)
    except ValueError:
        text = (response.text or "").strip()
        body = text or None
        # Surface a plain-text body as the message, but not HTML/XML error
        # pages (e.g. from a gateway), which would be noise.
        if text and not text.startswith("<"):
            message = text

    if not message:
        message = f"HTTP {status} {response.reason_phrase}".strip()

    return CapawesomeCloudError(
        message,
        status=status,
        status_text=response.reason_phrase or None,
        response=response,
        body=body,
    )


def _message_from_body(body: Any) -> Optional[str]:
    """Extract a human-readable message from an error response body.

    Handles the shapes the API (and its validation layer) can return:

    * a plain string body,
    * ``{"message": "..."}``,
    * ``{"error": "..."}``,
    * ``{"error": [{"path": [...], "message": "..."}]}``,
    * ``{"error": {"issues": [{"path": [...], "message": "..."}]}}``.
    """
    if isinstance(body, str):
        return body or None
    if not isinstance(body, dict):
        return None

    raw = body.get("message")
    if isinstance(raw, str) and raw:
        return raw

    errors = body.get("error")
    if isinstance(errors, str) and errors:
        return errors
    if isinstance(errors, dict):
        errors = errors.get("issues")
    if isinstance(errors, list):
        parts = []
        for item in errors:
            if not isinstance(item, dict):
                continue
            text = item.get("message")
            if not isinstance(text, str) or not text:
                continue
            path = item.get("path")
            if isinstance(path, list) and path:
                text = f"{'.'.join(str(segment) for segment in path)}: {text}"
            parts.append(text)
        if parts:
            return "; ".join(parts)

    return None
