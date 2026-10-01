"""Configurations resource (overwrite the native app configuration during builds)."""

from __future__ import annotations

from typing import List, Optional, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppConfiguration
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class ConfigurationsResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/configurations"

    def create(
        self,
        app_id: str,
        *,
        name: str,
        display_name: Union[str, None, NotGiven] = NOT_GIVEN,
        package_name: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> AppConfiguration:
        """Create a configuration.

        ``package_name`` is the Android package name or iOS bundle id.
        """
        body = build_body({"name": name, "displayName": display_name, "packageName": package_name})
        return self._request_model("POST", self._base(app_id), AppConfiguration, json=body)

    def list(
        self,
        app_id: str,
        *,
        name: Optional[str] = None,
        query: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppConfiguration]:
        """Iterate over all configurations of an app."""
        params = build_params({"name": name, "query": query})
        return self._paginate(
            self._base(app_id), AppConfiguration, params=params, page_size=page_size
        )

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[AppConfiguration]:
        """Fetch a single page of configurations."""
        params = build_params({"limit": limit, "offset": offset, "name": name, "query": query})
        return self._list_page(self._base(app_id), AppConfiguration, params=params)

    def get(self, app_id: str, configuration_id: str) -> AppConfiguration:
        """Retrieve a configuration by id."""
        return self._request_model(
            "GET", f"{self._base(app_id)}/{configuration_id}", AppConfiguration
        )

    def update(
        self,
        app_id: str,
        configuration_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        display_name: Union[str, None, NotGiven] = NOT_GIVEN,
        package_name: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> AppConfiguration:
        """Update a configuration."""
        body = build_body({"name": name, "displayName": display_name, "packageName": package_name})
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{configuration_id}", AppConfiguration, json=body
        )

    def delete(
        self, app_id: str, configuration_id: Optional[str] = None, *, name: Optional[str] = None
    ) -> None:
        """Delete a configuration by id or name. The id takes precedence."""
        self._delete_by_id_or_name(
            self._base(app_id), id=configuration_id, name=name, resource="configuration"
        )
