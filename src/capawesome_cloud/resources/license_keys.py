"""License keys resource (access to Capawesome Insiders packages)."""

from __future__ import annotations

from typing import List, Optional, Sequence, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import LicenseKey
from ._base import BaseResource, build_body, build_params, to_list


class LicenseKeysResource(BaseResource):
    def _base(self, organization_id: str) -> str:
        return f"/v1/organizations/{organization_id}/license-keys"

    def create(
        self,
        organization_id: str,
        *,
        name: str,
        package_ids: Union[Sequence[str], NotGiven] = NOT_GIVEN,
    ) -> LicenseKey:
        """Create a license key granting access to the given packages."""
        body = build_body({"name": name, "packageIds": to_list(package_ids)})
        return self._request_model("POST", self._base(organization_id), LicenseKey, json=body)

    def list(self, organization_id: str, *, relations: Optional[str] = None) -> List[LicenseKey]:
        """List all license keys of an organization.

        Pass ``relations="licenseKeyPackages,licenseKeyPackages.package"`` to
        include the assigned packages.
        """
        params = build_params({"relations": relations})
        return self._list_page(self._base(organization_id), LicenseKey, params=params)

    def get(
        self, organization_id: str, license_key_id: str, *, relations: Optional[str] = None
    ) -> LicenseKey:
        """Retrieve a license key by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(organization_id)}/{license_key_id}", LicenseKey, params=params
        )

    def update(
        self,
        organization_id: str,
        license_key_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        package_ids: Union[Sequence[str], NotGiven] = NOT_GIVEN,
    ) -> LicenseKey:
        """Update a license key.

        ``package_ids`` replaces the current assignments and cannot be changed
        while the license key is locked.
        """
        body = build_body({"name": name, "packageIds": to_list(package_ids)})
        return self._request_model(
            "PATCH", f"{self._base(organization_id)}/{license_key_id}", LicenseKey, json=body
        )

    def delete(self, organization_id: str, license_key_id: str) -> None:
        """Delete a license key."""
        self._request_none("DELETE", f"{self._base(organization_id)}/{license_key_id}")

    def rotate(self, organization_id: str, license_key_id: str) -> LicenseKey:
        """Rotate a license key. The previous key is invalidated immediately."""
        return self._request_model(
            "POST", f"{self._base(organization_id)}/{license_key_id}/rotate", LicenseKey
        )
