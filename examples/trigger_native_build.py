"""Trigger a native build, wait for it, and download its artifacts.

Run with:
    CAPAWESOME_CLOUD_TOKEN=cap_... python examples/trigger_native_build.py <app_id>
"""

from __future__ import annotations

import sys

from capawesome_cloud import CapawesomeCloud, JobTimeoutError


def main(app_id: str) -> None:
    with CapawesomeCloud() as client:
        build = client.apps.builds.create(app_id, platform="android")
        print(f"Started build {build.number_as_string} (job {build.job_id})")

        if not build.job_id:
            return

        try:
            job = client.jobs.wait(build.job_id, poll_interval=10, timeout=1800)
        except JobTimeoutError as error:
            print(error)
            return

        print(f"Build finished with status: {job.status}")
        if job.status != "succeeded":
            print(client.jobs.logs(build.job_id))
            return

        for artifact in client.apps.builds.artifacts.list(app_id, build.id):
            data = client.apps.builds.artifacts.download(app_id, build.id, artifact.id)
            filename = f"{artifact.type}-{artifact.id}.bin"
            with open(filename, "wb") as file:
                file.write(data)
            print(f"Downloaded {filename} ({len(data)} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: trigger_native_build.py <app_id>")
    main(sys.argv[1])
