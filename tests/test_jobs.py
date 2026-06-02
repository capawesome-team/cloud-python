from __future__ import annotations

import httpx
import pytest
import respx

from capawesome_cloud import CapawesomeCloud
from capawesome_cloud._http import DEFAULT_BASE_URL as BASE_URL


def test_wait_rejects_non_positive_poll_interval(client: CapawesomeCloud) -> None:
    with pytest.raises(ValueError, match="poll_interval"):
        client.jobs.wait("job1", poll_interval=0)


def test_wait_rejects_negative_timeout(client: CapawesomeCloud) -> None:
    with pytest.raises(ValueError, match="timeout"):
        client.jobs.wait("job1", timeout=-1)


@respx.mock
def test_wait_returns_on_terminal_status(client: CapawesomeCloud) -> None:
    route = respx.get(f"{BASE_URL}/v1/jobs/job1")
    route.side_effect = [
        httpx.Response(200, json={"id": "job1", "status": "in_progress"}),
        httpx.Response(200, json={"id": "job1", "status": "succeeded"}),
    ]
    job = client.jobs.wait("job1", poll_interval=0.01, timeout=5)
    assert job.status == "succeeded"
    assert route.call_count == 2
