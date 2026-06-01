"""Manage live-update channels and devices.

Run with:
    CAPAWESOME_CLOUD_TOKEN=cap_... python examples/manage_live_updates.py <app_id>
"""

from __future__ import annotations

import sys

from capawesome_cloud import CapawesomeCloud


def main(app_id: str) -> None:
    with CapawesomeCloud() as client:
        # Create (or reuse) a "staging" channel.
        channel = client.apps.channels.create(app_id, name="staging")
        print(f"Created channel {channel.name} ({channel.id})")

        # Pause and resume update delivery.
        client.apps.channels.pause(app_id, channel.id)
        print("Channel paused")
        client.apps.channels.resume(app_id, channel.id)
        print("Channel resumed")

        # List the most recently seen devices.
        print("Devices:")
        for device in client.apps.devices.list(app_id):
            print(f"  {device.id} - {device.app_version_name} ({device.os_version})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: manage_live_updates.py <app_id>")
    main(sys.argv[1])
