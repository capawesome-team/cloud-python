"""Trigger a native build, wait for it, and download its artifacts.

Run with:
    CAPAWESOME_CLOUD_TOKEN=cap_... python examples/trigger_native_build.py <app_id>
"""

from __future__ import annotations

import sys

from capawesome_cloud import CapawesomeCloud, JobTimeoutError


def main(app_id: str) -> None:
    with CapawesomeCloud() as client:
        # Builds need a source: a connected Git repo (pass git_ref) or an
        # uploaded build source (pass app_build_source_id).
        build = client.apps.builds.create(app_id, platform="android", git_ref="main")
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
            for log in client.jobs.logs(build.job_id):
                print(log.payload)
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
