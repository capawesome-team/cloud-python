"""Organizations resource and its organization-scoped sub-resources."""

from __future__ import annotations

from typing import List, Sequence, Union

from .._http import HttpClient
from .._types import NOT_GIVEN, NotGiven
from ..models import Organization
from ._base import BaseResource, build_body, to_list
from .git_connections import GitConnectionsResource
from .invitations import InvitationsResource
from .license_keys import LicenseKeysResource
from .members import MembersResource
from .teams import TeamsResource


class OrganizationsResource(BaseResource):
    """Organizations, plus all resources scoped under ``/v1/organizations/{organizationId}/...``.

    Organization-scoped resources are exposed as attributes
    (``client.organizations.members``, ``client.organizations.teams``, ...). Each
    of their methods takes ``organization_id`` as the first argument.
    """

    _path = "/v1/organizations"

    def __init__(self, http: HttpClient) -> None:
        super().__init__(http)
        self.git_connections = GitConnectionsResource(http)
        self.invitations = InvitationsResource(http)
        self.license_keys = LicenseKeysResource(http)
        self.members = MembersResource(http)
        self.teams = TeamsResource(http)

    def create(self, *, name: str, trial_code: Union[str, NotGiven] = NOT_GIVEN) -> Organization:
        """Create an organization, optionally redeeming a trial code."""
        body = build_body({"name": name, "trialCode": trial_code})
        return self._request_model("POST", self._path, Organization, json=body)

    def list(self) -> List[Organization]:
        """List the organizations the authenticated user is a member of."""
        return self._list_page(self._path, Organization)

    def get(self, organization_id: str) -> Organization:
        """Retrieve an organization by id."""
        return self._request_model("GET", f"{self._path}/{organization_id}", Organization)

    def update(
        self,
        organization_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        country_allowlist: Union[Sequence[str], None, NotGiven] = NOT_GIVEN,
        ip_allowlist: Union[Sequence[str], None, NotGiven] = NOT_GIVEN,
        two_factor_required: Union[bool, NotGiven] = NOT_GIVEN,
    ) -> Organization:
        """Update an organization.

        ``country_allowlist`` takes ISO 3166-1 alpha-2 codes and ``ip_allowlist``
        IP addresses or CIDR ranges. Pass ``None`` to allow all.
        """
        body = build_body(
            {
                "name": name,
                "countryAllowlist": to_list(country_allowlist),
                "ipAllowlist": to_list(ip_allowlist),
                "twoFactorRequired": two_factor_required,
            }
        )
        return self._request_model(
            "PATCH", f"{self._path}/{organization_id}", Organization, json=body
        )
