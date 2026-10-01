"""Shared functionality for resource clients."""

from __future__ import annotations

from typing import Any, List, Mapping, Optional, TypeVar

from .._http import HttpClient
from .._types import NotGiven
from ..models import CapawesomeModel
from ..pagination import DEFAULT_PAGE_SIZE, Paginator

T = TypeVar("T", bound=CapawesomeModel)


def build_body(values: Mapping[str, Any]) -> dict[str, Any]:
    """Drop :data:`NOT_GIVEN` entries, keeping explicit ``None`` values."""
    return {key: value for key, value in values.items() if not isinstance(value, NotGiven)}


def build_params(values: Mapping[str, Any]) -> dict[str, Any]:
    """Drop both :data:`NOT_GIVEN` and ``None`` query parameters."""
    return {
        key: value
        for key, value in values.items()
        if value is not None and not isinstance(value, NotGiven)
    }


class BaseResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    # -- single object ------------------------------------------------------

    def _request_model(
        self,
        method: str,
        path: str,
        model: type[T],
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
        files: Optional[Mapping[str, Any]] = None,
        data: Optional[Mapping[str, Any]] = None,
    ) -> T:
        payload = self._http.request_json(
            method, path, params=params, json=json, files=files, data=data
        )
        return model.model_validate(payload)

    def _request_none(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Optional[Any] = None,
    ) -> None:
        self._http.request(method, path, params=params, json=json)

    def _delete_by_id_or_name(
        self,
        collection_path: str,
        *,
        id: Optional[str],
        name: Optional[str],
        resource: str,
        params: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Delete by id, or by unique name if no id is given.

        ``params`` narrow down a name-based delete and are ignored for ids.
        """
        if id:
            self._request_none("DELETE", f"{collection_path}/{id}")
        elif name:
            self._request_none(
                "DELETE", collection_path, params=build_params({**(params or {}), "name": name})
            )
        else:
            raise ValueError(f"Either an id or a name is required to delete a {resource}.")

    # -- collections --------------------------------------------------------

    def _list_page(
        self,
        path: str,
        model: type[T],
        *,
        params: Optional[Mapping[str, Any]] = None,
    ) -> List[T]:
        payload = self._http.request_json("GET", path, params=params)
        items = payload if isinstance(payload, list) else []
        return [model.model_validate(item) for item in items]

    def _paginate(
        self,
        path: str,
        model: type[T],
        *,
        params: Optional[Mapping[str, Any]] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[T]:
        base_params = dict(params or {})

        def fetch(limit: int, offset: int) -> List[Any]:
            page_params = {**base_params, "limit": limit, "offset": offset}
            payload = self._http.request_json("GET", path, params=page_params)
            return payload if isinstance(payload, list) else []

        return Paginator(fetch, model, page_size=page_size)

    # -- binary -------------------------------------------------------------

    def _download(
        self,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
    ) -> bytes:
        response = self._http.request("GET", path, params=params)
        return response.content
