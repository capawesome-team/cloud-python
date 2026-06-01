"""Build sources resource."""

from __future__ import annotations

from typing import Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppBuildSource
from ._base import BaseResource, build_body


class BuildSourcesResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/build-sources"

    def create(
        self,
        app_id: str,
        *,
        file_url: Union[str, None, NotGiven] = NOT_GIVEN,
        file_size_in_bytes: Union[int, None, NotGiven] = NOT_GIVEN,
    ) -> AppBuildSource:
        """Create a build source (e.g. register an uploaded archive)."""
        body = build_body({"fileUrl": file_url, "fileSizeInBytes": file_size_in_bytes})
        return self._request_model("POST", self._base(app_id), AppBuildSource, json=body)

    def download(self, app_id: str, build_source_id: str) -> bytes:
        """Download a build source archive."""
        return self._download(f"{self._base(app_id)}/{build_source_id}/download")
