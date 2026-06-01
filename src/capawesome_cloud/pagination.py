"""Offset-based pagination.

List endpoints return a bare JSON array with no pagination metadata. Pages are
walked using ``limit`` / ``offset`` query parameters: a page shorter than the
requested ``page_size`` (or an empty page) marks the end.
"""

from __future__ import annotations

from typing import Any, Callable, Iterator, TypeVar

from .models import CapawesomeModel

T = TypeVar("T", bound=CapawesomeModel)

DEFAULT_PAGE_SIZE = 100

# A callable that fetches one raw page given (limit, offset).
PageFetcher = Callable[[int, int], list[Any]]


class Paginator(Iterator[T]):
    """Lazily iterates over every item across all pages.

    Iterate it directly to transparently page through the full result set::

        for channel in client.channels.list(app_id="..."):
            ...
    """

    def __init__(
        self,
        fetch_page: PageFetcher,
        model: type[T],
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
        start_offset: int = 0,
    ) -> None:
        if page_size < 1:
            raise ValueError("page_size must be >= 1")
        self._fetch_page = fetch_page
        self._model = model
        self._page_size = page_size
        self._offset = start_offset
        self._buffer: list[Any] = []
        self._exhausted = False

    def __iter__(self) -> Paginator[T]:
        return self

    def __next__(self) -> T:
        while not self._buffer:
            if self._exhausted:
                raise StopIteration
            self._load_next_page()
        item = self._buffer.pop(0)
        return self._model.model_validate(item)

    def _load_next_page(self) -> None:
        page = self._fetch_page(self._page_size, self._offset)
        if not page:
            self._exhausted = True
            return
        self._buffer.extend(page)
        self._offset += len(page)
        if len(page) < self._page_size:
            self._exhausted = True

    def to_list(self) -> list[T]:
        """Eagerly fetch and return every item as a list."""
        return list(self)
