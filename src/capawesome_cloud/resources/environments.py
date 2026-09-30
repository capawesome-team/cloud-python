"""Environments resource, including variables and secrets."""

from __future__ import annotations

from typing import List, Optional, Union

from .._http import HttpClient
from .._types import NOT_GIVEN, NotGiven
from ..models import AppEnvironment, AppEnvironmentSecret, AppEnvironmentVariable
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class EnvironmentsResource(BaseResource):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http)
        self.variables = EnvironmentVariablesResource(http)
        self.secrets = EnvironmentSecretsResource(http)

    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/environments"

    def create(self, app_id: str, *, name: str) -> AppEnvironment:
        """Create an environment."""
        return self._request_model("POST", self._base(app_id), AppEnvironment, json={"name": name})

    def list(
        self,
        app_id: str,
        *,
        name: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppEnvironment]:
        """Iterate over all environments of an app."""
        params = build_params({"name": name, "query": query, "relations": relations})
        return self._paginate(
            self._base(app_id), AppEnvironment, params=params, page_size=page_size
        )

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppEnvironment]:
        """Fetch a single page of environments."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "name": name,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppEnvironment, params=params)

    def get(
        self, app_id: str, environment_id: str, *, relations: Optional[str] = None
    ) -> AppEnvironment:
        """Retrieve an environment by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{environment_id}", AppEnvironment, params=params
        )

    def update(self, app_id: str, environment_id: str, *, name: str) -> AppEnvironment:
        """Update an environment."""
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{environment_id}", AppEnvironment, json={"name": name}
        )

    def delete(
        self, app_id: str, environment_id: Optional[str] = None, *, name: Optional[str] = None
    ) -> None:
        """Delete an environment by id or name. The id takes precedence."""
        self._delete_by_id_or_name(
            self._base(app_id), id=environment_id, name=name, resource="environment"
        )


class EnvironmentVariablesResource(BaseResource):
    def _base(self, app_id: str, environment_id: str) -> str:
        return f"/v1/apps/{app_id}/environments/{environment_id}/variables"

    def create(
        self, app_id: str, environment_id: str, *, key: str, value: str
    ) -> AppEnvironmentVariable:
        """Create an environment variable."""
        return self._request_model(
            "POST",
            self._base(app_id, environment_id),
            AppEnvironmentVariable,
            json={"key": key, "value": value},
        )

    def list(self, app_id: str, environment_id: str) -> List[AppEnvironmentVariable]:
        """List all variables of an environment."""
        return self._list_page(self._base(app_id, environment_id), AppEnvironmentVariable)

    def update(
        self,
        app_id: str,
        environment_id: str,
        variable_id: str,
        *,
        key: Union[str, NotGiven] = NOT_GIVEN,
        value: Union[str, NotGiven] = NOT_GIVEN,
    ) -> AppEnvironmentVariable:
        """Update an environment variable."""
        body = build_body({"key": key, "value": value})
        return self._request_model(
            "PATCH",
            f"{self._base(app_id, environment_id)}/{variable_id}",
            AppEnvironmentVariable,
            json=body,
        )

    def delete(self, app_id: str, environment_id: str, variable_id: str) -> None:
        """Delete an environment variable."""
        self._request_none("DELETE", f"{self._base(app_id, environment_id)}/{variable_id}")


class EnvironmentSecretsResource(BaseResource):
    def _base(self, app_id: str, environment_id: str) -> str:
        return f"/v1/apps/{app_id}/environments/{environment_id}/secrets"

    def create(
        self, app_id: str, environment_id: str, *, key: str, value: str
    ) -> AppEnvironmentSecret:
        """Create an environment secret."""
        return self._request_model(
            "POST",
            self._base(app_id, environment_id),
            AppEnvironmentSecret,
            json={"key": key, "value": value},
        )

    def list(self, app_id: str, environment_id: str) -> List[AppEnvironmentSecret]:
        """List all secrets of an environment (values are not returned)."""
        return self._list_page(self._base(app_id, environment_id), AppEnvironmentSecret)

    def update(
        self,
        app_id: str,
        environment_id: str,
        secret_id: str,
        *,
        key: Union[str, NotGiven] = NOT_GIVEN,
        value: Union[str, NotGiven] = NOT_GIVEN,
    ) -> AppEnvironmentSecret:
        """Update an environment secret."""
        body = build_body({"key": key, "value": value})
        return self._request_model(
            "PATCH",
            f"{self._base(app_id, environment_id)}/{secret_id}",
            AppEnvironmentSecret,
            json=body,
        )

    def delete(self, app_id: str, environment_id: str, secret_id: str) -> None:
        """Delete an environment secret."""
        self._request_none("DELETE", f"{self._base(app_id, environment_id)}/{secret_id}")
