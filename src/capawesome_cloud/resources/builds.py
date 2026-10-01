"""Builds resource (Native Builds) and build artifacts."""

from __future__ import annotations

from typing import Any, List, Mapping, Optional, Sequence, Union

from .._http import HttpClient
from .._types import NOT_GIVEN, NotGiven
from ..models import AppBuild, AppBuildArtifact
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params, to_list


class BuildsResource(BaseResource):
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http)
        self.artifacts = BuildArtifactsResource(http)

    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/builds"

    def create(
        self,
        app_id: str,
        *,
        platform: Union[str, None, NotGiven] = NOT_GIVEN,
        type: Union[str, None, NotGiven] = NOT_GIVEN,
        stack: Union[str, NotGiven] = NOT_GIVEN,
        git_ref: Union[str, None, NotGiven] = NOT_GIVEN,
        app_build_source_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_certificate_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_certificate_name: Union[str, None, NotGiven] = NOT_GIVEN,
        app_channel_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_channel_ids: Union[Sequence[str], None, NotGiven] = NOT_GIVEN,
        app_channel_names: Union[Sequence[str], None, NotGiven] = NOT_GIVEN,
        app_configuration_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_configuration_name: Union[str, None, NotGiven] = NOT_GIVEN,
        app_destination_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_environment_id: Union[str, None, NotGiven] = NOT_GIVEN,
        app_environment_name: Union[str, None, NotGiven] = NOT_GIVEN,
        ad_hoc_environment_variables: Union[Mapping[str, str], None, NotGiven] = NOT_GIVEN,
        release_notes: Union[Mapping[str, str], NotGiven] = NOT_GIVEN,
    ) -> AppBuild:
        """Trigger a native build. Returns the build (poll its ``job_id`` for progress).

        Web builds are deployed to the channels in ``app_channel_ids`` (or
        ``app_channel_names``) after they succeed; ``app_channel_id`` is deprecated.
        ``release_notes`` are only supported together with ``app_destination_id``
        (see :meth:`DeploymentsResource.create`).
        """
        body = build_body(
            {
                "platform": platform,
                "type": type,
                "stack": stack,
                "gitRef": git_ref,
                "appBuildSourceId": app_build_source_id,
                "appCertificateId": app_certificate_id,
                "appCertificateName": app_certificate_name,
                "appChannelId": app_channel_id,
                "appChannelIds": to_list(app_channel_ids),
                "appChannelNames": to_list(app_channel_names),
                "appConfigurationId": app_configuration_id,
                "appConfigurationName": app_configuration_name,
                "appDestinationId": app_destination_id,
                "appEnvironmentId": app_environment_id,
                "appEnvironmentName": app_environment_name,
                "adHocEnvironmentVariables": ad_hoc_environment_variables,
                "releaseNotes": release_notes,
            }
        )
        return self._request_model("POST", self._base(app_id), AppBuild, json=body)

    def list(
        self,
        app_id: str,
        *,
        platform: Optional[str] = None,
        app_automation_id: Optional[str] = None,
        app_git_commit: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppBuild]:
        """Iterate over all builds of an app."""
        params = build_params(
            {
                "platform": platform,
                "appAutomationId": app_automation_id,
                "appGitCommit": app_git_commit,
                "query": query,
                "relations": relations,
            }
        )
        return self._paginate(self._base(app_id), AppBuild, params=params, page_size=page_size)

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        platform: Optional[str] = None,
        app_automation_id: Optional[str] = None,
        app_git_commit: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppBuild]:
        """Fetch a single page of builds."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "platform": platform,
                "appAutomationId": app_automation_id,
                "appGitCommit": app_git_commit,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppBuild, params=params)

    def get(self, app_id: str, build_id: str, *, relations: Optional[str] = None) -> AppBuild:
        """Retrieve a build by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{build_id}", AppBuild, params=params
        )

    def update(
        self,
        app_id: str,
        build_id: str,
        *,
        display_name: Union[str, None, NotGiven] = NOT_GIVEN,
        package_name: Union[str, None, NotGiven] = NOT_GIVEN,
        package_version: Union[str, None, NotGiven] = NOT_GIVEN,
        custom_properties: Union[Mapping[str, Any], None, NotGiven] = NOT_GIVEN,
    ) -> AppBuild:
        """Update build metadata."""
        body = build_body(
            {
                "displayName": display_name,
                "packageName": package_name,
                "packageVersion": package_version,
                "customProperties": custom_properties,
            }
        )
        return self._request_model("PATCH", f"{self._base(app_id)}/{build_id}", AppBuild, json=body)


class BuildArtifactsResource(BaseResource):
    def _base(self, app_id: str, build_id: str) -> str:
        return f"/v1/apps/{app_id}/builds/{build_id}/artifacts"

    def list(
        self,
        app_id: str,
        build_id: str,
        *,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppBuildArtifact]:
        """Iterate over all artifacts of a build."""
        params = build_params({"relations": relations})
        return self._paginate(
            self._base(app_id, build_id), AppBuildArtifact, params=params, page_size=page_size
        )

    def list_page(
        self,
        app_id: str,
        build_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        relations: Optional[str] = None,
    ) -> List[AppBuildArtifact]:
        """Fetch a single page of build artifacts."""
        params = build_params({"limit": limit, "offset": offset, "relations": relations})
        return self._list_page(self._base(app_id, build_id), AppBuildArtifact, params=params)

    def get_download_url(
        self,
        app_id: str,
        build_id: str,
        artifact_id: str,
        *,
        file_name: Optional[str] = None,
    ) -> Any:
        """Return the signed download URL payload for an artifact."""
        params = build_params({"fileName": file_name})
        return self._http.request_json(
            "GET",
            f"{self._base(app_id, build_id)}/{artifact_id}/signed-download-url",
            params=params,
        )

    def download(
        self,
        app_id: str,
        build_id: str,
        artifact_id: str,
        *,
        file_name: Optional[str] = None,
    ) -> bytes:
        """Download an artifact's bytes."""
        params = build_params({"fileName": file_name})
        return self._download(
            f"{self._base(app_id, build_id)}/{artifact_id}/download", params=params
        )
