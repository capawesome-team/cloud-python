from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx
import pytest
import respx

from capawesome_cloud import CapawesomeCloud, CapawesomeCloudError
from capawesome_cloud._http import DEFAULT_BASE_URL as BASE_URL
from capawesome_cloud._http import _parse_retry_after


@respx.mock
def test_error_message_and_status_are_extracted(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps/missing").mock(
        return_value=httpx.Response(404, json={"message": "App not found."})
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.get("missing")
    assert excinfo.value.message == "App not found."
    assert excinfo.value.status == 404
    assert excinfo.value.status_text == "Not Found"


@respx.mock
def test_validation_error_message_is_extracted(client: CapawesomeCloud) -> None:
    respx.post(f"{BASE_URL}/v1/apps/app1/builds").mock(
        return_value=httpx.Response(
            400,
            json={
                "success": False,
                "data": {"platform": "android"},
                "error": [
                    {
                        "code": "custom",
                        "path": [],
                        "message": "Either gitRef or appBuildSourceId must be provided.",
                    }
                ],
            },
        )
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.builds.create("app1", platform="android")
    assert excinfo.value.message == "Either gitRef or appBuildSourceId must be provided."
    assert excinfo.value.status == 400
    # The full raw body is still available.
    assert excinfo.value.body["success"] is False


@respx.mock
def test_validation_error_includes_field_path(client: CapawesomeCloud) -> None:
    respx.post(f"{BASE_URL}/v1/apps/app1/builds").mock(
        return_value=httpx.Response(
            400,
            json={"error": [{"path": ["platform"], "message": "Invalid value."}]},
        )
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.builds.create("app1", platform="bogus")
    assert excinfo.value.message == "platform: Invalid value."


@respx.mock
def test_zod_issues_error_message(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps/x").mock(
        return_value=httpx.Response(
            400, json={"error": {"issues": [{"path": ["name"], "message": "Required."}]}}
        )
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.get("x")
    assert excinfo.value.message == "name: Required."


@respx.mock
def test_plain_text_error_body_is_used_as_message(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps/x").mock(
        return_value=httpx.Response(400, text="Something went wrong")
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.get("x")
    assert excinfo.value.message == "Something went wrong"


@respx.mock
def test_html_error_body_is_not_used_as_message(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps/x").mock(
        return_value=httpx.Response(502, html="<html><body>Bad Gateway</body></html>")
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.get("x")
    assert excinfo.value.message == "HTTP 502 Bad Gateway"


@respx.mock
def test_401_carries_status(client: CapawesomeCloud) -> None:
    respx.get(f"{BASE_URL}/v1/apps").mock(
        return_value=httpx.Response(401, json={"message": "Not authenticated."})
    )
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.list_page()
    assert excinfo.value.status == 401


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
    with pytest.raises(CapawesomeCloudError) as excinfo:
        client.apps.list_page()
    assert excinfo.value.status == 503
    assert route.call_count == 2  # initial + 1 retry


@respx.mock
def test_post_not_retried_on_5xx() -> None:
    # A non-idempotent POST must not be retried on 5xx (it may have been
    # processed server-side -- retrying could duplicate the side effect).
    client = CapawesomeCloud(token="t", max_retries=3, backoff_factor=0.0)
    route = respx.post(f"{BASE_URL}/v1/apps").mock(
        return_value=httpx.Response(503, json={"message": "unavailable"})
    )
    with pytest.raises(CapawesomeCloudError):
        client.apps.create(name="App")
    assert route.call_count == 1


@respx.mock
def test_post_is_retried_on_429() -> None:
    # 429 means the request was rejected before processing, so it is safe to
    # retry even a POST.
    client = CapawesomeCloud(token="t", max_retries=2, backoff_factor=0.0)
    route = respx.post(f"{BASE_URL}/v1/apps")
    route.side_effect = [
        httpx.Response(429, json={"message": "slow down"}),
        httpx.Response(201, json={"id": "a1", "name": "App"}),
    ]
    app = client.apps.create(name="App")
    assert app.id == "a1"
    assert route.call_count == 2


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
