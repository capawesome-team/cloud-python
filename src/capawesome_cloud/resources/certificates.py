"""Certificates resource (signing certificates / keystores)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import IO, List, Optional, Union

from .._types import NOT_GIVEN, NotGiven
from ..models import AppCertificate
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_body, build_params

FileSource = Union[str, "os.PathLike[str]", bytes, IO[bytes]]


class CertificatesResource(BaseResource):
    def _base(self, app_id: str) -> str:
        return f"/v1/apps/{app_id}/certificates"

    def create(
        self,
        app_id: str,
        *,
        name: str,
        file: FileSource,
        file_name: Optional[str] = None,
        platform: Union[str, None, NotGiven] = NOT_GIVEN,
        type: Union[str, NotGiven] = NOT_GIVEN,
        password: Union[str, NotGiven] = NOT_GIVEN,
        key_alias: Union[str, NotGiven] = NOT_GIVEN,
        key_password: Union[str, NotGiven] = NOT_GIVEN,
    ) -> AppCertificate:
        """Upload a signing certificate.

        ``file`` may be a path, raw ``bytes``, or an open binary file object.
        ``type`` is ``development`` or ``production``.
        """
        content, resolved_name = _read_file(file, file_name)
        data = build_body(
            {
                "name": name,
                "platform": platform,
                "type": type,
                "password": password,
                "keyAlias": key_alias,
                "keyPassword": key_password,
            }
        )
        files = {"file": (resolved_name, content)}
        return self._request_model(
            "POST", self._base(app_id), AppCertificate, data=data, files=files
        )

    def list(
        self,
        app_id: str,
        *,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        type: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[AppCertificate]:
        """Iterate over all certificates of an app."""
        params = build_params(
            {
                "name": name,
                "platform": platform,
                "type": type,
                "query": query,
                "relations": relations,
            }
        )
        return self._paginate(
            self._base(app_id), AppCertificate, params=params, page_size=page_size
        )

    def list_page(
        self,
        app_id: str,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        type: Optional[str] = None,
        query: Optional[str] = None,
        relations: Optional[str] = None,
    ) -> List[AppCertificate]:
        """Fetch a single page of certificates."""
        params = build_params(
            {
                "limit": limit,
                "offset": offset,
                "name": name,
                "platform": platform,
                "type": type,
                "query": query,
                "relations": relations,
            }
        )
        return self._list_page(self._base(app_id), AppCertificate, params=params)

    def get(
        self, app_id: str, certificate_id: str, *, relations: Optional[str] = None
    ) -> AppCertificate:
        """Retrieve a certificate by id."""
        params = build_params({"relations": relations})
        return self._request_model(
            "GET", f"{self._base(app_id)}/{certificate_id}", AppCertificate, params=params
        )

    def update(
        self,
        app_id: str,
        certificate_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        type: Union[str, NotGiven] = NOT_GIVEN,
        password: Union[str, None, NotGiven] = NOT_GIVEN,
        key_alias: Union[str, None, NotGiven] = NOT_GIVEN,
        key_password: Union[str, None, NotGiven] = NOT_GIVEN,
    ) -> AppCertificate:
        """Update a certificate's metadata."""
        body = build_body(
            {
                "name": name,
                "type": type,
                "password": password,
                "keyAlias": key_alias,
                "keyPassword": key_password,
            }
        )
        return self._request_model(
            "PATCH", f"{self._base(app_id)}/{certificate_id}", AppCertificate, json=body
        )

    def delete(self, app_id: str, certificate_id: str) -> None:
        """Delete a certificate."""
        self._request_none("DELETE", f"{self._base(app_id)}/{certificate_id}")


def _read_file(file: FileSource, file_name: Optional[str]) -> tuple[bytes, str]:
    if isinstance(file, (str, os.PathLike)):
        path = Path(file)
        return path.read_bytes(), file_name or path.name
    if isinstance(file, bytes):
        return file, file_name or "certificate"
    content = file.read()
    name = file_name or getattr(file, "name", None) or "certificate"
    return content, os.path.basename(str(name))
