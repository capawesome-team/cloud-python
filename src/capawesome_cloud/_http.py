"""Low-level HTTP transport used by every resource.

Wraps an :class:`httpx.Client` and adds:

* bearer-token authentication,
* automatic retries with exponential backoff on ``429`` and ``5xx`` responses,
* mapping of error responses to the SDK exception hierarchy.
"""

from __future__ import annotations

import time
from typing import Any, Mapping, Optional

import httpx

from ._version import __version__
from .exceptions import (
    APIConnectionError,
    APITimeoutError,
    exception_from_response,
)

DEFAULT_BASE_URL = "https://api.cloud.capawesome.io"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_BACKOFF_FACTOR = 0.5

_RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# A small JSON-ish type. Responses are intentionally loosely typed because the
# API does not publish response schemas.
JSON = Any


class HttpClient:
    """Thin, retrying wrapper around :class:`httpx.Client`."""

    def __init__(
        self,
        *,
        token: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
        )
        # The token must always apply; identify ourselves on clients we create
        # without clobbering a caller-supplied client's User-Agent.
        self._client.headers["Authorization"] = f"Bearer {token}"
        self._client.headers.setdefault("Accept", "application/json")
        if self._owns_client:
            self._client.headers["User-Agent"] = f"capawesome-cloud-python/{__version__}"

    # -- public API ---------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        files: Optional[Mapping[str, Any]] = None,
        data: Optional[Mapping[str, Any]] = None,
    ) -> httpx.Response:
        """Send a request, retrying transient failures, and validate the status."""
        clean_params = _drop_none(params) if params else None
        attempt = 0
        while True:
            try:
                response = self._client.request(
                    method,
                    path,
                    params=clean_params,
                    json=json,
                    files=files,
                    data=data,
                )
            except httpx.TimeoutException as exc:
                if attempt < self._max_retries:
                    self._sleep(attempt, None)
                    attempt += 1
                    continue
                raise APITimeoutError(request=exc.request) from exc
            except httpx.TransportError as exc:
                if attempt < self._max_retries:
                    self._sleep(attempt, None)
                    attempt += 1
                    continue
                raise APIConnectionError(str(exc), request=exc.request) from exc

            if response.status_code in _RETRY_STATUS_CODES and attempt < self._max_retries:
                self._sleep(attempt, response)
                attempt += 1
                continue

            if response.is_success:
                return response

            raise exception_from_response(response)

    def request_json(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        files: Optional[Mapping[str, Any]] = None,
        data: Optional[Mapping[str, Any]] = None,
    ) -> JSON:
        """Send a request and return the parsed JSON body (``None`` if empty)."""
        response = self.request(method, path, params=params, json=json, files=files, data=data)
        if not response.content:
            return None
        return response.json()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- internals ----------------------------------------------------------

    def _sleep(self, attempt: int, response: Optional[httpx.Response]) -> None:
        delay = self._backoff_factor * (2**attempt)
        if response is not None:
            retry_after = _parse_retry_after(response.headers.get("Retry-After"))
            if retry_after is not None:
                delay = max(delay, retry_after)
        time.sleep(delay)


def _drop_none(mapping: Mapping[str, Any]) -> dict[str, Any]:
    """Return a copy of ``mapping`` without ``None`` values."""
    return {key: value for key, value in mapping.items() if value is not None}


def _parse_retry_after(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None
