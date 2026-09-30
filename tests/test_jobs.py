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


@respx.mock
def test_list_joins_multiple_statuses(client: CapawesomeCloud) -> None:
    route = respx.get(f"{BASE_URL}/v1/jobs").mock(return_value=httpx.Response(200, json=[]))
    client.jobs.list_page(organization_id="org1", status=["queued", "in_progress"])
    assert route.calls.last.request.url.params["status"] == "queued,in_progress"


@respx.mock
def test_cancel(client: CapawesomeCloud) -> None:
    route = respx.patch(f"{BASE_URL}/v1/jobs/job1").mock(
        return_value=httpx.Response(200, json={"id": "job1", "status": "canceled"})
    )
    job = client.jobs.cancel("job1")
    assert route.calls.last.request.read() == b'{"status":"canceled"}'
    assert job.status == "canceled"


@respx.mock
def test_get_failure_summary(client: CapawesomeCloud) -> None:
    respx.post(f"{BASE_URL}/v1/jobs/job1/failure-summary").mock(
        return_value=httpx.Response(200, json={"summary": "The signing certificate expired."})
    )
    assert client.jobs.get_failure_summary("job1").summary == "The signing certificate expired."
