"""Automations resource."""

from __future__ import annotations

from typing import List, Optional

from .._types import NotGiven
from ..models import AppAutomation
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_params

_WRITE_FIELDS = {
    "name": "name",
    "trigger_type": "triggerType",
    "trigger_pattern": "triggerPattern",
    "commit_message_pattern": "commitMessagePattern",
    "platform": "platform",
    "build_type": "buildType",
    "build_stack": "buildStack",
    "enabled": "enabled",
    "app_certificate_id": "appCertificateId",
    "app_channel_id": "appChannelId",
    "app_destination_id": "appDestinationId",
    "app_environment_id": "appEnvironmentId",
}


class AutomationsResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/automations"

    def create(
        self, app_id: str, *, name: str, trigger_type: str, **fields: object
    ) -> AppAutomation:
        """Create an automation.

        ``name`` and ``trigger_type`` (``branch`` or ``tag``) are required. Provide
        further fields by their snake_case names (e.g. ``platform``,
        ``trigger_pattern``, ``app_channel_id``).
        """
        body = _map_write_fields({"name": name, "trigger_type": trigger_type, **fields})
        return self._request_model("POST", self._base(app_id), AppAutomation, json=body)

    def list(
        self,
        app_id: str,
        *,
        platform: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppAutomation]:
        """Iterate over all automations of an app."""
        params = build_params({"platform": platform, "query": query, "relations": relations})
        return self._paginate(self._base(app_id), AppAutomation, params=params, page_size=page_size)

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        platform: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppAutomation]:
        """Fetch a single page of automations."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "platform": platform,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppAutomation, params=params)

    def get(
        self, app_id: str, automation_id: str, *, relations: Optional[str] = None
    ) -> AppAutomation:
        """Retrieve an automation by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{automation_id}", AppAutomation, params=params
        )

    def update(self, app_id: str, automation_id: str, **fields: object) -> AppAutomation:
        """Update an automation. Provide fields by their snake_case names."""
        body = _map_write_fields(fields)
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{automation_id}", AppAutomation, json=body
        )

    def delete(self, app_id: str, automation_id: str) -> None:
        """Delete an automation."""
        self._request_none("DELETE", f"{self._base(app_id)}/{automation_id}")


def _map_write_fields(fields: dict[str, object]) -> dict[str, object]:
    body: dict[str, object] = {}
    for key, value in fields.items():
        if isinstance(value, NotGiven):
            continue
        api_key = _WRITE_FIELDS.get(key)
        if api_key is None:
            raise TypeError(f"Unknown automation field: {key!r}")
        body[api_key] = value
    return body
