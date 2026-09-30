"""Channels resource (Live Updates)."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppChannel
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class ChannelsResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/channels"

    def create(
        self,
        app_id: str,
        *,
        name: str,
        protected: Union[bool, NotGiven] = NOT_GIVEN,
        expires_at: Union[datetime, str, None, NotGiven] = NOT_GIVEN,
    ) -> AppChannel:
        """Create a channel."""
        body = build_body(
            {"name": name, "protected": protected, "expiresAt": _isoformat(expires_at)}
        )
        return self._request_model("POST", self._base(app_id), AppChannel, json=body)

    def list(
        self,
        app_id: str,
        *,
        name: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppChannel]:
        """Iterate over all channels of an app."""
        params = build_params({"name": name, "query": query, "relations": relations})
        return self._paginate(self._base(app_id), AppChannel, params=params, page_size=page_size)

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppChannel]:
        """Fetch a single page of channels."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "name": name,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppChannel, params=params)

    def get(self, app_id: str, channel_id: str) -> AppChannel:
        """Retrieve a channel by id."""
        return self._request_model("GET", f"{self._base(app_id)}/{channel_id}", AppChannel)

    def update(
        self,
        app_id: str,
        channel_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        protected: Union[bool, NotGiven] = NOT_GIVEN,
        expires_at: Union[datetime, str, None, NotGiven] = NOT_GIVEN,
    ) -> AppChannel:
        """Update a channel."""
        body = build_body(
            {"name": name, "protected": protected, "expiresAt": _isoformat(expires_at)}
        )
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{channel_id}", AppChannel, json=body
        )

    def delete(
        self, app_id: str, channel_id: Optional[str] = None, *, name: Optional[str] = None
    ) -> None:
        """Delete a channel by id or name. The id takes precedence."""
        self._delete_by_id_or_name(self._base(app_id), id=channel_id, name=name, resource="channel")

    def pause(self, app_id: str, channel_id: str) -> None:
        """Pause update delivery on a channel."""
        self._request_none("POST", f"{self._base(app_id)}/{channel_id}/pause")

    def resume(self, app_id: str, channel_id: str) -> None:
        """Resume update delivery on a channel."""
        self._request_none("POST", f"{self._base(app_id)}/{channel_id}/resume")


def _isoformat(value: object) -> object:
    if isinstance(value, datetime):
        return value.isoformat()
    return value
