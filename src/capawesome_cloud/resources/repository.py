"""Repository resource (the Git repository an app is linked to)."""

from __future__ import annotations

from ..models import App, AppGitRepository
from ._base import BaseResource


class RepositoryResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/repository"

    def get(self, app_id: str) -> AppGitRepository:
        """Retrieve the repository an app is linked to."""
        return self._request_model("GET", self._base(app_id), AppGitRepository)

    def set(self, app_id: str, *, git_connection_id: str, path: str) -> App:
        """Link an app to a repository, replacing the current link.

        ``path`` is the repository path as used by the provider, e.g. ``owner/name``.
        """
        return self._request_model(
            "PUT",
            self._base(app_id),
            App,
            json={"gitConnectionId": git_connection_id, "path": path},
        )

    def delete(self, app_id: str) -> None:
        """Unlink an app from its repository."""
        self._request_none("DELETE", self._base(app_id))
