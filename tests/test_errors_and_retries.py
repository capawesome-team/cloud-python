from __future__ import annotations

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
