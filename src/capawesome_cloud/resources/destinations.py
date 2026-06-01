"""Destinations resource (App Store Publishing targets)."""

from __future__ import annotations

from typing import List, Optional

from .._types import NotGiven
from ..models import AppDestination
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_params

# Fields shared by create and update.
_WRITE_FIELDS = {
    "name": "name",
    "platform": "platform",
    "android_build_artifact_type": "androidBuildArtifactType",
    "android_package_name": "androidPackageName",
    "android_release_status": "androidReleaseStatus",
    "google_play_track": "googlePlayTrack",
    "app_apple_api_key_id": "appAppleApiKeyId",
    "app_google_service_account_key_id": "appGoogleServiceAccountKeyId",
    "apple_api_key_id": "appleApiKeyId",
    "apple_issuer_id": "appleIssuerId",
    "apple_id": "appleId",
    "apple_app_password": "appleAppPassword",
    "apple_app_id": "appleAppId",
    "apple_team_id": "appleTeamId",
}


class DestinationsResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/destinations"

    def create(self, app_id: str, *, name: str, **fields: object) -> AppDestination:
        """Create a destination.

        ``name`` is required. Provide further fields by their snake_case names,
        e.g. ``platform``, ``android_package_name``, ``apple_app_id``,
        ``google_play_track`` (see the API reference for the full list).
        """
        body = _map_write_fields({"name": name, **fields})
        return self._request_model("POST", self._base(app_id), AppDestination, json=body)

    def list(
        self,
        app_id: str,
        *,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppDestination]:
        """Iterate over all destinations of an app."""
        params = build_params(
            {"name": name, "platform": platform, "query": query, "relations": relations}
        )
        return self._paginate(
            self._base(app_id), AppDestination, params=params, page_size=page_size
        )

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppDestination]:
        """Fetch a single page of destinations."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "name": name,
                "platform": platform,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppDestination, params=params)

    def get(
        self, app_id: str, destination_id: str, *, relations: Optional[str] = None
    ) -> AppDestination:
        """Retrieve a destination by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{destination_id}", AppDestination, params=params
        )

    def update(self, app_id: str, destination_id: str, **fields: object) -> AppDestination:
        """Update a destination. Provide fields by their snake_case names."""
        body = _map_write_fields(fields)
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{destination_id}", AppDestination, json=body
        )

    def delete(self, app_id: str, destination_id: str) -> None:
        """Delete a destination."""
        self._request_none("DELETE", f"{self._base(app_id)}/{destination_id}")


def _map_write_fields(fields: dict[str, object]) -> dict[str, object]:
    body: dict[str, object] = {}
    for key, value in fields.items():
        if isinstance(value, NotGiven):
            continue
        api_key = _WRITE_FIELDS.get(key)
        if api_key is None:
            raise TypeError(f"Unknown destination field: {key!r}")
        body[api_key] = value
    return body
