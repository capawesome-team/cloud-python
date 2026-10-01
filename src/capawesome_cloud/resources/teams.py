"""Teams resource, including team apps and team members."""

from __future__ import annotations

from typing import List, Optional, Union

from .._http import HttpClient
from .._types import NOT_GIVEN, NotGiven
from ..models import Team, TeamApp, TeamMember
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class TeamsResource(BaseResource):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http)
        self.apps = TeamAppsResource(http)
        self.members = TeamMembersResource(http)

    def _base(self, organization_id: str) -> str:
        return f"/v1/organizations/{organization_id}/teams"

    def create(
        self,
        organization_id: str,
        *,
        name: str,
        description: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> Team:
        """Create a team."""
        body = build_body({"name": name, "description": description})
        return self._request_model("POST", self._base(organization_id), Team, json=body)

    def list(
        self,
        organization_id: str,
        *,
        name: Optional[str] = None,
        query: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[Team]:
        """Iterate over all teams of an organization."""
        params = build_params({"name": name, "query": query})
        return self._paginate(self._base(organization_id), Team, params=params, page_size=page_size)

    def list_page(
        self,
        organization_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[Team]:
        """Fetch a single page of teams."""
        params = build_params({"limit": limit, "offset": offset, "name": name, "query": query})
        return self._list_page(self._base(organization_id), Team, params=params)

    def get(self, organization_id: str, team_id: str, *, relations: Optional[str] = None) -> Team:
        """Retrieve a team by id.

        Pass ``relations="apps,members"`` to include the team's apps and members.
        """
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(organization_id)}/{team_id}", Team, params=params
        )

    def update(
        self,
        organization_id: str,
        team_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> None:
        """Update a team."""
        body = build_body({"name": name, "description": description})
        self._request_none("PATCH", f"{self._base(organization_id)}/{team_id}", json=body)

    def delete(self, organization_id: str, team_id: str) -> None:
        """Delete a team."""
        self._request_none("DELETE", f"{self._base(organization_id)}/{team_id}")


class TeamAppsResource(BaseResource):
    def _base(self, organization_id: str, team_id: str) -> str:
        return f"/v1/organizations/{organization_id}/teams/{team_id}/apps"

    def create(self, organization_id: str, team_id: str, *, app_id: str) -> TeamApp:
        """Assign an app to a team."""
        return self._request_model(
            "POST", self._base(organization_id, team_id), TeamApp, json={"appId": app_id}
        )

    def list(
        self,
        organization_id: str,
        team_id: str,
        *,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[TeamApp]:
        """Iterate over all apps of a team."""
        params = build_params({"relations": relations})
        return self._paginate(
            self._base(organization_id, team_id), TeamApp, params=params, page_size=page_size
        )

    def list_page(
        self,
        organization_id: str,
        team_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        relations: Optional[str] = None,
    ) -> List[TeamApp]:
        """Fetch a single page of team apps."""
        params = build_params({"limit": limit, "offset": offset, "relations": relations})
        return self._list_page(self._base(organization_id, team_id), TeamApp, params=params)

    def delete(self, organization_id: str, team_id: str, team_app_id: str) -> None:
        """Remove an app from a team."""
        self._request_none("DELETE", f"{self._base(organization_id, team_id)}/{team_app_id}")


class TeamMembersResource(BaseResource):
    def _base(self, organization_id: str, team_id: str) -> str:
        return f"/v1/organizations/{organization_id}/teams/{team_id}/members"

    def create(self, organization_id: str, team_id: str, *, member_id: str) -> TeamMember:
        """Add an organization member to a team."""
        return self._request_model(
            "POST",
            self._base(organization_id, team_id),
            TeamMember,
            json={"memberId": member_id},
        )

    def list(
        self,
        organization_id: str,
        team_id: str,
        *,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[TeamMember]:
        """Iterate over all members of a team."""
        params = build_params({"relations": relations})
        return self._paginate(
            self._base(organization_id, team_id), TeamMember, params=params, page_size=page_size
        )

    def list_page(
        self,
        organization_id: str,
        team_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        relations: Optional[str] = None,
    ) -> List[TeamMember]:
        """Fetch a single page of team members."""
        params = build_params({"limit": limit, "offset": offset, "relations": relations})
        return self._list_page(self._base(organization_id, team_id), TeamMember, params=params)

    def delete(self, organization_id: str, team_id: str, team_member_id: str) -> None:
        """Remove a member from a team."""
        self._request_none("DELETE", f"{self._base(organization_id, team_id)}/{team_member_id}")
