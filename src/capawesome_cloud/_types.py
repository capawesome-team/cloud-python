"""Shared sentinel types."""

from __future__ import annotations

from typing import Literal


class NotGiven:
    """Sentinel marking an omitted argument.

    Distinguishes "argument not provided" from an explicit ``None``. This lets a
    caller send ``null`` to clear a field (pass ``None``) versus leaving it
    untouched (pass nothing).
    """

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()
