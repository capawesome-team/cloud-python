"""Devices resource (Live Updates)."""

from __future__ import annotations

from typing import List, Optional, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppDevice
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class DevicesResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/devices"

    def list(
        self,
        app_id: str,
        *,
        id: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppDevice]:
        """Iterate over all devices of an app."""
        params = build_params({"id": id, "query": query, "relations": relations})
        return self._paginate(self._base(app_id), AppDevice, params=params, page_size=page_size)

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        id: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppDevice]:
        """Fetch a single page of devices."""
        params = build_params(
            {"limit": limit, "offset": offset, "id": id, "query": query, "relations": relations}
        )
        return self._list_page(self._base(app_id), AppDevice, params=params)

    def get(self, app_id: str, device_id: str, *, relations: Optional[str] = None) -> AppDevice:
        """Retrieve a device by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{device_id}", AppDevice, params=params
        )

    def update(
        self,
        app_id: str,
        device_id: str,
        *,
        forced_app_channel_id: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> AppDevice:
        """Update a device (e.g. pin it to a channel, or pass ``None`` to unpin)."""
        body = build_body({"forcedAppChannelId": forced_app_channel_id})
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{device_id}", AppDevice, json=body
        )

    def delete(self, app_id: str, device_id: str) -> None:
        """Delete a device."""
        self._request_none("DELETE", f"{self._base(app_id)}/{device_id}")
