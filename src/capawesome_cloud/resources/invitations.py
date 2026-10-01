"""Invitations resource (invite users to an organization)."""

from __future__ import annotations

from typing import List, Optional

from ..models import OrganizationInvitation
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_params


class InvitationsResource(BaseResource):
    def _base(self, organization_id: str) -> str:
        return f"/v1/organizations/{organization_id}/invitations"

    def create(self, organization_id: str, *, email: str, role: str) -> OrganizationInvitation:
        """Invite a user. ``role`` is one of ``admin``, ``billing``, ``member``, ``viewer``."""
        return self._request_model(
            "POST",
            self._base(organization_id),
            OrganizationInvitation,
            json={"email": email, "role": role},
        )

    def list(
        self,
        organization_id: str,
        *,
        query: Optional[str] = None,
        role: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[OrganizationInvitation]:
        """Iterate over all invitations of an organization."""
        params = build_params({"query": query, "role": role})
        return self._paginate(
            self._base(organization_id), OrganizationInvitation, params=params, page_size=page_size
        )

    def list_page(
        self,
        organization_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        query: Optional[str] = None,
        role: Optional[str] = None,
    ) -> List[OrganizationInvitation]:
        """Fetch a single page of invitations."""
        params = build_params({"limit": limit, "offset": offset, "query": query, "role": role})
        return self._list_page(self._base(organization_id), OrganizationInvitation, params=params)

    def delete(self, organization_id: str, invitation_id: str) -> None:
        """Revoke an invitation."""
        self._request_none("DELETE", f"{self._base(organization_id)}/{invitation_id}")
