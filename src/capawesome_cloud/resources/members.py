"""Members resource (organization members)."""

from __future__ import annotations

from typing import List, Optional

from ..models import OrganizationMember
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_params


class MembersResource(BaseResource):
    def _base(self, organization_id: str) -> str:
        return f"/v1/organizations/{organization_id}/members"

    def list(
        self,
        organization_id: str,
        *,
        id: Optional[str] = None,
        query: Optional[str] = None,
        role: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[OrganizationMember]:
        """Iterate over all members of an organization.

        ``role`` is one of ``owner``, ``admin``, ``billing``, ``member``, ``viewer``.
        """
        params = build_params({"id": id, "query": query, "role": role})
        return self._paginate(
            self._base(organization_id), OrganizationMember, params=params, page_size=page_size
        )

    def list_page(
        self,
        organization_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        id: Optional[str] = None,
        query: Optional[str] = None,
        role: Optional[str] = None,
    ) -> List[OrganizationMember]:
        """Fetch a single page of members."""
        params = build_params(
            {"limit": limit, "offset": offset, "id": id, "query": query, "role": role}
        )
        return self._list_page(self._base(organization_id), OrganizationMember, params=params)

    def delete(self, organization_id: str, member_id: str) -> None:
        """Remove a member from an organization."""
        self._request_none("DELETE", f"{self._base(organization_id)}/{member_id}")
