"""Deployments resource (publish a build to a channel or app-store destination)."""

from __future__ import annotations

from typing import List, Mapping, Optional, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppDeployment
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params


class DeploymentsResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/deployments"

    def create(
        self,
        app_id: str,
        *,
        app_build_id: str,
        app_channel_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_channel_name: Union[str, None, NotGiven] = NOT_GIVEN,
        app_destination_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_destination_name: Union[str, None, NotGiven] = NOT_GIVEN,
        rollout_percentage: Union[float, None, NotGiven] = NOT_GIVEN,
        release_notes: Union[Mapping[str, str], NotGiven] = NOT_GIVEN,
    ) -> AppDeployment:
        """Create a deployment. Target a live-update channel and/or a destination.

        ``release_notes`` are only supported for destination deployments. They
        require a ``default`` entry; other keys are locales (e.g. ``de-DE``) with
        translations. Google Play and Huawei AppGallery allow 500 characters per
        entry, other destinations 4000.
        """
        body = build_body(
            {
                "appBuildId": app_build_id,
                "appChannelId": app_channel_id,
                "appChannelName": app_channel_name,
                "appDestinationId": app_destination_id,
                "appDestinationName": app_destination_name,
                "rolloutPercentage": rollout_percentage,
                "releaseNotes": release_notes,
            }
        )
        return self._request_model("POST", self._base(app_id), AppDeployment, json=body)

    def list(
        self,
        app_id: str,
        *,
        app_build_id: Optional[str] = None,
        app_channel_id: Optional[str] = None,
        app_destination_id: Optional[str] = None,
        app_git_commit: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppDeployment]:
        """Iterate over all deployments of an app."""
        params = build_params(
            {
                "appBuildId": app_build_id,
                "appChannelId": app_channel_id,
                "appDestinationId": app_destination_id,
                "appGitCommit": app_git_commit,
                "query": query,
                "relations": relations,
            }
        )
        return self._paginate(self._base(app_id), AppDeployment, params=params, page_size=page_size)

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        app_build_id: Optional[str] = None,
        app_channel_id: Optional[str] = None,
        app_destination_id: Optional[str] = None,
        app_git_commit: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppDeployment]:
        """Fetch a single page of deployments."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "appBuildId": app_build_id,
                "appChannelId": app_channel_id,
                "appDestinationId": app_destination_id,
                "appGitCommit": app_git_commit,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppDeployment, params=params)

    def get(
        self, app_id: str, deployment_id: str, *, relations: Optional[str] = None
    ) -> AppDeployment:
        """Retrieve a deployment by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{deployment_id}", AppDeployment, params=params
        )

    def update(
        self, app_id: str, deployment_id: str, *, rollout_percentage: float
    ) -> AppDeployment:
        """Update a deployment's rollout percentage (0-1)."""
        return self._request_model(
            "PATCH",
            f"{self._base(app_id)}/{deployment_id}",
            AppDeployment,
            json={"rolloutPercentage": rollout_percentage},
        )
