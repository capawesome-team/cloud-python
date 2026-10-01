"""Jobs resource (track async builds and deployments)."""

from __future__ import annotations

import time
from typing import List, Optional, Sequence, Union

from ..exceptions import CapawesomeCloudError
from ..models import Job, JobFailureSummary, JobLog
from ..pagination import DEFAULT_PAGE_SIZE, Paginator
from ._base import BaseResource, build_params

#: Statuses that mean a job has stopped running.
TERMINAL_STATUSES = frozenset({"succeeded", "failed", "canceled", "rejected", "timed_out"})


class JobTimeoutError(CapawesomeCloudError):
    """Raised when :meth:`JobsResource.wait` exceeds its timeout."""


class JobsResource(BaseResource):
    _path = "/v1/jobs"

    def list(
        self,
        *,
        organization_id: str,
        status: Union[str, Sequence[str], None] = None,
        relations: Optional[str] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Paginator[Job]:
        """Iterate over all jobs of an organization."""
        params = build_params(
            {
                "organizationId": organization_id,
                "status": _join_statuses(status),
                "relations": relations,
            }
        )
        return self._paginate(self._path, Job, params=params, page_size=page_size)

    def list_page(
        self,
        *,
        organization_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Union[str, Sequence[str], None] = None,
        relations: Optional[str] = None,
    ) -> List[Job]:
        """Fetch a single page of jobs."""
        params = build_params(
            {
                "organizationId": organization_id,
                "limit": limit,
                "offset": offset,
                "status": _join_statuses(status),
                "relations": relations,
            }
        )
        return self._list_page(self._path, Job, params=params)

    def get(self, job_id: str, *, relations: Optional[str] = None) -> Job:
        """Retrieve a job by id."""
        params = build_params({"relations": relations})
        return self._request_model("GET", f"{self._path}/{job_id}", Job, params=params)

    def logs(self, job_id: str) -> List[JobLog]:
        """List the log lines of a job."""
        return self._list_page(f"{self._path}/{job_id}/logs", JobLog)

    def get_failure_summary(self, job_id: str) -> JobFailureSummary:
        """Return a summary explaining why a failed job failed.

        The summary is generated on the first request and cached afterwards.
        """
        return self._request_model(
            "POST", f"{self._path}/{job_id}/failure-summary", JobFailureSummary
        )

    def cancel(self, job_id: str) -> Job:
        """Cancel a job that has not finished yet."""
        return self._request_model(
            "PATCH", f"{self._path}/{job_id}", Job, json={"status": "canceled"}
        )

    def wait(
        self,
        job_id: str,
        *,
        poll_interval: float = 5.0,
        timeout: Optional[float] = 600.0,
    ) -> Job:
        """Poll a job until it reaches a terminal status and return it.

        Raises :class:`JobTimeoutError` if ``timeout`` seconds elapse first.
        Pass ``timeout=None`` to wait indefinitely.
        """
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")
        if timeout is not None and timeout < 0:
            raise ValueError("timeout must be >= 0 or None")
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            job = self.get(job_id)
            if job.status in TERMINAL_STATUSES:
                return job
            if deadline is not None and time.monotonic() + poll_interval > deadline:
                raise JobTimeoutError(
                    f"Job {job_id} did not finish within {timeout} seconds "
                    f"(last status: {job.status})."
                )
            time.sleep(poll_interval)


def _join_statuses(status: Union[str, Sequence[str], None]) -> Optional[str]:
    if status is None or isinstance(status, str):
        return status
    return ",".join(status)
