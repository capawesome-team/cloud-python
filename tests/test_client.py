from __future__ import annotations

import httpx
import pytest

from capawesome_cloud import CapawesomeCloud, CapawesomeCloudError


def test_token_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CAPAWESOME_CLOUD_TOKEN", "from-env")
    client = CapawesomeCloud()
    assert client._http._client.headers["Authorization"] == "Bearer from-env"


def test_missing_token_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CAPAWESOME_CLOUD_TOKEN", raising=False)
    with pytest.raises(CapawesomeCloudError, match="No API token"):
        CapawesomeCloud()


def test_sets_auth_and_user_agent_headers() -> None:
    client = CapawesomeCloud(token="abc")
    headers = client._http._client.headers
    assert headers["Authorization"] == "Bearer abc"
    assert headers["User-Agent"].startswith("capawesome-cloud-python/")


def test_context_manager_closes() -> None:
    with CapawesomeCloud(token="abc") as client:
        underlying: httpx.Client = client._http._client
    assert underlying.is_closed
