"""Users resource."""

from __future__ import annotations

from ..models import User
from ._base import BaseResource


class UsersResource(BaseResource):
    _path = "/v1/users"

    def me(self) -> User:
        """Retrieve the user the token belongs to."""
        return self._request_model("GET", f"{self._path}/me", User)
