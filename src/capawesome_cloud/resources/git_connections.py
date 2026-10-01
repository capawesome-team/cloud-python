"""Git connections resource (access Git providers and browse repositories)."""

from __future__ import annotations

from typing import List, Optional, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import GitConnection, GitNamespace, GitRepository
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class GitConnectionsResource(BaseResource):
    def _base(self, organization_id: str) -> str:
        return f"/v1/organizations/{organization_id}/git-connections"

    def create(
        self,
        organization_id: str,
        *,
        provider: str,
        auth_kind: str,
        name: Union[str, NotGiven] = NOT_GIVEN,
        base_url: Union[str, NotGiven] = NOT_GIVEN,
        token: Union[str, NotGiven] = NOT_GIVEN,
        username: Union[str, NotGiven] = NOT_GIVEN,
        password: Union[str, NotGiven] = NOT_GIVEN,
        user_provider_profile_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> GitConnection:
        """Create a Git connection.

        ``provider`` is one of ``azure_devops``, ``bitbucket``, ``gitea``,
        ``git_http``, ``github``, ``gitlab``. ``auth_kind`` is one of ``basic``
        (``username`` and ``password``), ``oauth`` (``user_provider_profile_id``)
        or ``token``. ``base_url`` points to a self-hosted provider.
        """
        body = build_body(
            {
                "provider": provider,
                "authKind": auth_kind,
                "name": name,
                "baseUrl": base_url,
                "token": token,
                "username": username,
                "password": password,
                "userProviderProfileId": user_provider_profile_id,
            }
        )
        return self._request_model("POST", self._base(organization_id), GitConnection, json=body)

    def list(
        self,
        organization_id: str,
        *,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        query: Optional[str] = None,
        restricted: Optional[bool] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[GitConnection]:
        """Iterate over all Git connections of an organization."""
        params = build_params(
            {
                "name": name,
                "provider": provider,
                "query": query,
                "restricted": restricted,
                "relations": relations,
            }
        )
        return self._paginate(
            self._base(organization_id), GitConnection, params=params, page_size=page_size
        )

    def list_page(
        self,
        organization_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        query: Optional[str] = None,
        restricted: Optional[bool] = None,
        relations: Optional[str] = None,
    ) -> List[GitConnection]:
        """Fetch a single page of Git connections."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "name": name,
                "provider": provider,
                "query": query,
                "restricted": restricted,
                "relations": relations,
            }
        )
        return self._list_page(self._base(organization_id), GitConnection, params=params)

    def get(
        self, organization_id: str, git_connection_id: str, *, relations: Optional[str] = None
    ) -> GitConnection:
        """Retrieve a Git connection by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET",
            f"{self._base(organization_id)}/{git_connection_id}",
            GitConnection,
            params=params,
        )

    def update(
        self,
        organization_id: str,
        git_connection_id: str,
        *,
        auth_kind: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        base_url: Union[str, None, NotGiven] = NOT_GIVEN,
        token: Union[str, NotGiven] = NOT_GIVEN,
        username: Union[str, NotGiven] = NOT_GIVEN,
        password: Union[str, NotGiven] = NOT_GIVEN,
    ) -> GitConnection:
        """Update a Git connection. ``auth_kind`` is ``basic`` or ``token``."""
        body = build_body(
            {
                "authKind": auth_kind,
                "name": name,
                "baseUrl": base_url,
                "token": token,
                "username": username,
                "password": password,
            }
        )
        return self._request_model(
            "PATCH", f"{self._base(organization_id)}/{git_connection_id}", GitConnection, json=body
        )

    def delete(self, organization_id: str, git_connection_id: str) -> None:
        """Delete a Git connection."""
        self._request_none("DELETE", f"{self._base(organization_id)}/{git_connection_id}")

    def list_repositories(
        self,
        organization_id: str,
        git_connection_id: str,
        *,
        namespace: Optional[str] = None,
        path: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[GitRepository]:
        """List the repositories accessible through a Git connection."""
        params = build_params({"namespace": namespace, "path": path, "query": query})
        return self._list_page(
            f"{self._base(organization_id)}/{git_connection_id}/repositories",
            GitRepository,
            params=params,
        )

    def list_namespaces(
        self,
        organization_id: str,
        git_connection_id: str,
        *,
        organization: Optional[str] = None,
    ) -> List[GitNamespace]:
        """List the namespaces (users, organizations, groups, ...) of a Git connection."""
        params = build_params({"organization": organization})
        return self._list_page(
            f"{self._base(organization_id)}/{git_connection_id}/namespaces",
            GitNamespace,
            params=params,
        )
