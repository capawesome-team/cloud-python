"""The main Capawesome Cloud client."""

from __future__ import annotations

import os
from typing import Optional

import httpx

from ._http import (
    DEFAULT_BACKOFF_FACTOR,
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    HttpClient,
)
from .exceptions import CapawesomeCloudError
from .resources import AppsResource, JobsResource, UsersResource

# Token environment variables, in order of precedence. CAPAWESOME_TOKEN is
# accepted for consistency with the Capawesome CLI.
ENV_TOKENS = ("CAPAWESOME_CLOUD_TOKEN", "CAPAWESOME_TOKEN")


class CapawesomeCloud:
    """Synchronous client for the Capawesome Cloud API.

    Create an API token in the Capawesome Cloud Console
    (https://console.cloud.capawesome.io/settings/tokens) and pass it as
    ``token`` or via the ``CAPAWESOME_CLOUD_TOKEN`` (or ``CAPAWESOME_TOKEN``)
    environment variable.

    Example::

        from capawesome_cloud import CapawesomeCloud

        client = CapawesomeCloud(token="...")
        for app in client.apps.list():
            print(app.id, app.name)
    """

    def __init__(
        self,
        token: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        resolved_token = token
        for env_name in ENV_TOKENS:
            if resolved_token:
                break
            resolved_token = os.environ.get(env_name)
        # Trim surrounding whitespace/newlines (common with secrets piped from
        # files or CI) so they don't break the Authorization header.
        resolved_token = (resolved_token or "").strip()
        if not resolved_token:
            raise CapawesomeCloudError(
                "No API token provided. Pass token=... or set the "
                f"{ENV_TOKENS[0]} environment variable."
            )

        self._http = HttpClient(
            token=resolved_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            http_client=http_client,
        )

        # App-scoped resources are nested under ``apps`` (e.g.
        # ``client.apps.channels``); ``jobs`` is organization-scoped.
        self.apps = AppsResource(self._http)
        self.jobs = JobsResource(self._http)
        self.users = UsersResource(self._http)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> CapawesomeCloud:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
