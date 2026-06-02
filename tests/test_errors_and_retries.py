from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx
import pytest
import respx

from capawesome_cloud import (
    AuthenticationError,
    CapawesomeCloud,
    InternalServerError,
    NotFoundError,
)
from capawesome_cloud._http import DEFAULT_BASE_URL as BASE_URL
from capawesome_cloud._http import _parse_retry_after


@respx.mock
def test_error_message_is_extracted(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps/missing").mock(
        return_value=httpx.Response(404, json={"message": "App not found."})
    )
    with pytest.raises(NotFoundError) as excinfo:
        client.apps.get("missing")
    assert excinfo.value.message == "App not found."
    assert excinfo.value.status_code == 404


@respx.mock
def test_401_maps_to_authentication_error(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps").mock(
        return_value=httpx.Response(401, json={"message": "Not authenticated."})
    )
    with pytest.raises(AuthenticationError):
        client.apps.list_page()


@respx.mock
def test_retries_on_429_then_succeeds() -> None:
    client = CapawesomeCloud(token="t", max_retries=2, backoff_factor=0.0)
    route = respx.get(f"{BASE_URL}/v1/apps")
    route.side_effect = [
        httpx.Response(429, json={"message": "slow down"}),
        httpx.Response(200, json=[{"id": "a1", "name": "App"}]),
    ]
    apps = client.apps.list_page()
    assert route.call_count == 2
    assert [a.id for a in apps] == ["a1"]


@respx.mock
def test_gives_up_after_max_retries() -> None:
    client = CapawesomeCloud(token="t", max_retries=1, backoff_factor=0.0)
    route = respx.get(f"{BASE_URL}/v1/apps").mock(
        return_value=httpx.Response(503, json={"message": "unavailable"})
    )
    with pytest.raises(InternalServerError):
        client.apps.list_page()
    assert route.call_count == 2  # initial + 1 retry


def test_parse_retry_after_seconds() -> None:
    assert _parse_retry_after("5") == 5.0
    assert _parse_retry_after(" 5 ") == 5.0
    # Negative seconds are clamped to zero.
    assert _parse_retry_after("-3") == 0.0


def test_parse_retry_after_http_date() -> None:
    future = datetime.now(timezone.utc) + timedelta(seconds=30)
    delay = _parse_retry_after(format_datetime(future))
    assert delay is not None
    assert 25 <= delay <= 31
    # A date in the past clamps to zero rather than going negative.
    past = datetime.now(timezone.utc) - timedelta(seconds=30)
    assert _parse_retry_after(format_datetime(past)) == 0.0


def test_parse_retry_after_invalid() -> None:
    assert _parse_retry_after(None) is None
    assert _parse_retry_after("") is None
    assert _parse_retry_after("not-a-date") is None
