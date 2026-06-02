"""Webhooks resource."""

from __future__ import annotations

from typing import List, Optional, Sequence, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppWebhook
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class WebhooksResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/webhooks"

    def create(
        self,
        app_id: str,
        *,
        name: str,
        url: str,
        events: Sequence[str],
        format: Union[str, NotGiven] = NOT_GIVEN,
        signing_secret: Union[str, NotGiven] = NOT_GIVEN,
    ) -> AppWebhook:
        """Create a webhook. ``format`` is one of ``raw``, ``discord``, ``slack``, ``teams``."""
        body = build_body(
            {
                "name": name,
                "url": url,
                "events": list(events),
                "format": format,
                "signingSecret": signing_secret,
            }
        )
        return self._request_model("POST", self._base(app_id), AppWebhook, json=body)

    def list(
        self,
        app_id: str,
        *,
        query: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppWebhook]:
        """Iterate over all webhooks of an app."""
        params = build_params({"query": query})
        return self._paginate(self._base(app_id), AppWebhook, params=params, page_size=page_size)

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        query: Optional[str] = None,
    ) -> List[AppWebhook]:
        """Fetch a single page of webhooks."""
        params = build_params({"limit": limit, "offset": offset, "query": query})
        return self._list_page(self._base(app_id), AppWebhook, params=params)

    def get(self, app_id: str, webhook_id: str) -> AppWebhook:
        """Retrieve a webhook by id."""
        return self._request_model("GET", f"{self._base(app_id)}/{webhook_id}", AppWebhook)

    def update(
        self,
        app_id: str,
        webhook_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        url: Union[str, NotGiven] = NOT_GIVEN,
        events: Union[Sequence[str], NotGiven] = NOT_GIVEN,
        format: Union[str, NotGiven] = NOT_GIVEN,
        enabled: Union[bool, NotGiven] = NOT_GIVEN,
        signing_secret: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> AppWebhook:
        """Update a webhook."""
        body = build_body(
            {
                "name": name,
                "url": url,
                "events": list(events) if not isinstance(events, NotGiven) else events,
                "format": format,
                "enabled": enabled,
                "signingSecret": signing_secret,
            }
        )
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{webhook_id}", AppWebhook, json=body
        )

    def delete(self, app_id: str, webhook_id: str) -> None:
        """Delete a webhook."""
        self._request_none("DELETE", f"{self._base(app_id)}/{webhook_id}")
